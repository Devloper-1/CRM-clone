from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend import models, database
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.logging_config import logger

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# 👇 DB session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ GET /tasks — Smart filtering by id, status, client_id
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    # Apply filters only if they are provided
    if id:
        query = query.filter(models.Task.id == id)
    if status:
        query = query.filter(models.Task.status == status)
    if client_id:
        query = query.filter(models.Task.client_id == client_id)

    tasks = query.all()
    return tasks


# ✅ POST /tasks — Create a new task (status is REQUIRED now)
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Check if the client exists
    db_client = db.query(models.Client).filter(models.Client.id == task.client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Create the task with required fields
    db_task = models.Task(
        client_id=task.client_id,
        description=task.description,
        status=task.status  # status is required now, no default
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info(f"Task {db_task.id} created successfully")

    return db_task


# ✅ PUT /tasks/{task_id} — Update a task by ID
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)
    logger.info(f"Task {task_id} updated successfully")

    return db_task


# ✅ DELETE /tasks — Delete one or many using flexible filters
@router.delete("/")
def delete_tasks(
    task_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    # Delete single task by ID
    if task_id:
        db_task = query.filter(models.Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(db_task)
        db.commit()
        logger.info(f"Task {task_id} deleted successfully")
        return {"detail": f"Task {task_id} deleted"}

    # Bulk delete using filters
    if status:
        query = query.filter(models.Task.status == status)
    if client_id:
        query = query.filter(models.Task.client_id == client_id)

    deleted_count = query.delete(synchronize_session=False)
    db.commit()
    logger.info(f"{deleted_count} tasks deleted by filter")

    return {"detail": f"{deleted_count} tasks deleted"}

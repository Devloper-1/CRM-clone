from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, database
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.logging_config import logger

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET all tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

# CREATE a new task
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        description=task.description,
        status=task.status or "pending",  # default if status not given
        client_id=task.client_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# UPDATE a task
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        db_task.status = task.status
    if task.client_id is not None:
        db_task.client_id = task.client_id

    db.commit()
    db.refresh(db_task)
    logger.info(f"✅ Task {task_id} updated successfully")

    return db_task

# DELETE a task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    logger.info(f"🗑️ Task {task_id} deleted successfully")

    return {"detail": "Task deleted"}

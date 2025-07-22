from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, database
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.logging_config import logger

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == task.client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_task = models.Task(
        client_id=task.client_id,
        description=task.description,
        status=task.status or "pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info(f"Task {db_task.id} created successfully")

    return db_task



@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description

    db.commit()
    db.refresh(db_task)
    logger.info(f"Task {task_id} updated successfully")

    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    logger.info(f"Task {task_id} deleted successfully")

    return {"detail": "Task deleted"}

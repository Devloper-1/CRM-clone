# ================================
# 📂 backend/routers/tasks.py
# ================================

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional , List
from backend import models
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.database import get_db
from backend.utils.auth_utils import verify_token
from fastapi.responses import StreamingResponse
import io
import csv

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(verify_token)]
      )

# ================================
# Login Token
# ================================
@router.get("/tasks")
def get_tasks(token: str=Depends(verify_token) , db: Session= Depends(get_db)):
    tasks= db.query(models.Task).all()
    return tasks

# ================================
# 1️⃣ Get Tasks
# ================================
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Fetch all tasks or filter by ID / Client ID"""
    query = db.query(models.Task)
    if id:
        query = query.filter(models.Task.id == id)
    if client_id:
        query = query.filter(models.Task.client_id == client_id)
    return query.all()


# ================================
# 2️⃣ Create Task
# ================================
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# ================================
# 3️⃣ Update Task by ID
# ================================
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """Update task details"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


# ================================
# 4️⃣ Delete Task by ID
# ================================
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by its ID"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}

# ================================
# 5️⃣ Export Tasks to CSV
# ================================
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
     """Export all tasks as a CSV file"""
     tasks = db.query(models.Task).all()

     # Use an in-memory buffer
     buffer = io.StringIO()
     writer = csv.writer(buffer)

      # Write CSV header
     writer.writerow(["id","client_id","description","status"])

     # Write task rows
     for task in tasks :
         writer.writerow([
           task.id ,
           task.client_id,
           task.description,
           task.status
         ])
     buffer.seek(0)
     return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks.csv"}
    )

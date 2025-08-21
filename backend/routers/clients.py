# ================================
# 📂 backend/routers/clients.py
# ================================

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional

from backend import models
from backend.schemas import ClientCreate, ClientUpdate, ClientResponse
from backend.database import get_db

router = APIRouter(prefix="/clients", tags=["Clients"])


# ================================
# 1️⃣ Get Clients
# ================================
@router.get("/", response_model=list[ClientResponse])
def get_clients(
    id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Fetch all clients or filter by ID / User ID"""
    query = db.query(models.Client)
    if id:
        query = query.filter(models.Client.id == id)
    if user_id:
        query = query.filter(models.Client.user_id == user_id)
    return query.all()


# ================================
# 2️⃣ Create Client
# ================================
@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client"""
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# ================================
# 3️⃣ Update Client by ID
# ================================
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_update: ClientUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """Update client details"""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in client_update.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


# ================================
# 4️⃣ Delete Client by ID
# ================================
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Delete a client by its ID"""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(db_client)
    db.commit()
    return {"message": f"Client {client_id} deleted"}

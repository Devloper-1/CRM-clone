from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend import models, database
from backend.schemas import ClientCreate, ClientUpdate, ClientResponse
from backend.logging_config import logger

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ GET /clients — filter by id or user_id
@router.get("/", response_model=list[ClientResponse])
def get_clients(
    id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Client)

    if id:
        query = query.filter(models.Client.id == id)
    if user_id:
        query = query.filter(models.Client.user_id == user_id)

    return query.all()

# ✅ POST /clients — create with required fields
@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(
        user_id=client.user_id,
        name=client.name,
        email=client.email,
        phone=client.phone
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info(f"Client {db_client.id} created successfully")
    return db_client

# ✅ PUT /clients/{id} — update by ID
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client.name is not None:
        db_client.name = client.name
    if client.email is not None:
        db_client.email = client.email
    if client.phone is not None:
        db_client.phone = client.phone

    db.commit()
    db.refresh(db_client)
    logger.info(f"Client {client_id} updated successfully")
    return db_client

# ✅ DELETE /clients — delete by id or user_id
@router.delete("/")
def delete_clients(
    client_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Client)

    if client_id:
        db_client = query.filter(models.Client.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        db.delete(db_client)
        db.commit()
        return {"detail": f"Client {client_id} deleted"}

    if user_id:
        deleted_count = query.filter(models.Client.user_id == user_id).delete(synchronize_session=False)
        db.commit()
        return {"detail": f"{deleted_count} clients deleted"}

    raise HTTPException(status_code=400, detail="Provide client_id or user_id for deletion")

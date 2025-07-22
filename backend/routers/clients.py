from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(
        name=client.name,
        email=client.email,
        phone=client.phone,
        user_id=client.user_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


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


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    logger.info(f"Client {client_id} deleted successfully")

    return {"detail": "Client deleted"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend import models, database
from backend.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from backend.logging_config import logger

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PaymentResponse])
def get_payments(
    id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Payment)
    if id:
        query = query.filter(models.Payment.id == id)
    if task_id:
        query = query.filter(models.Payment.task_id == task_id)
    if client_id:
        query = query.filter(models.Payment.client_id == client_id)
    return query.all()

@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = models.Payment(
        task_id=payment.task_id,
        client_id=payment.client_id,
        amount=payment.amount,
        status=payment.status
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    logger.info(f"Payment {db_payment.id} created successfully")
    return db_payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.amount is not None:
        db_payment.amount = payment.amount
    if payment.status is not None:
        db_payment.status = payment.status
    db.commit()
    db.refresh(db_payment)
    logger.info(f"Payment {payment_id} updated successfully")
    return db_payment

@router.delete("/")
def delete_payment(
    payment_id: Optional[int] = Query(None),
    task_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Payment)
    if payment_id:
        db_payment = query.filter(models.Payment.id == payment_id).first()
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        db.delete(db_payment)
        db.commit()
        return {"detail": f"Payment {payment_id} deleted"}
    if task_id:
        deleted = query.filter(models.Payment.task_id == task_id).delete(synchronize_session=False)
        db.commit()
        return {"detail": f"{deleted} payments deleted"}
    if client_id:
        deleted = query.filter(models.Payment.client_id == client_id).delete(synchronize_session=False)
        db.commit()
        return {"detail": f"{deleted} payments deleted"}
    raise HTTPException(status_code=400, detail="Provide payment_id, task_id, or client_id for deletion")

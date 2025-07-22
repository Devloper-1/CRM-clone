from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, database
from backend.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from backend.logging_config import logger

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(models.Payment).all()

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.amount is not None:
        db_payment.amount = payment.amount

    db.commit()
    db.refresh(db_payment)
    logger.info(f"Payment {payment_id} updated successfully")

    return db_payment

@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == payment.client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_payment = models.Payment(
        client_id=payment.client_id,
        amount=payment.amount,
        status=payment.status or "pending"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    logger.info(f"Payment {db_payment.id} created successfully")

    return db_payment



@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    logger.info(f"Payment {payment_id} deleted successfully")

    return {"detail": "Payment deleted"}

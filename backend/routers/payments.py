# ================================
# 📂 backend/routers/payments.py
# ================================

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional , List
from backend import models
from backend.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from backend.database import get_db
from backend.utils.auth_utils import create_access_token, verify_token
from fastapi.responses import StreamingResponse
import io
import csv 


# ✅ Router setup
router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    dependencies=[Depends(verify_token)]
      )

# ================================
# 1️⃣ Get Payments (with token)
# ================================
@router.get("/", response_model=list[PaymentResponse])
def get_payments(
    id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Fetch all payments or filter by ID / Client ID"""
    query = db.query(models.Payment)
    if id:
        query = query.filter(models.Payment.id == id)
    if client_id:
        query = query.filter(models.Payment.client_id == client_id)
    return query.all()


# ================================
# 2️⃣ Create Payment
# ================================
@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Create a new payment"""
    db_payment = models.Payment(**payment.model_dump())  # ✅ Pydantic v2
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


# ================================
# 3️⃣ Update Payment by ID
# ================================
@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate = Body(...),  # ✅ Explicit body parse
    db: Session = Depends(get_db)
):
    """Update a payment by its ID"""
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # ✅ Pydantic v2 style for partial updates
    for key, value in payment_update.model_dump(exclude_unset=True).items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment


# ================================
# 4️⃣ Delete Payment by ID
# ================================
@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Delete a payment by its ID"""
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(db_payment)
    db.commit()
    return {"message": f"Payment {payment_id} deleted"}


# ================================
# 5️⃣ Export Payments to CSV
# ================================
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """Export all payments as a CSV file """
    payments = db.query(models.Payment).all()

    # Use Stringio (text buffer)
    buffer = io.StringIO()
    writer = csv.writer(buffer , lineterminator='\n')

    # write payment rows
    for payment in payments :
        writer.writerow([
             payment.id ,
             payment.client_id ,
             payment.task_id,
             payment.amount,
             payment.status,
             payment.created_at
             ])
    #  Convert text buffer to bytes
    buffer_bytes = io.BytesIO(buffer.getvalue().encode('utf-8'))
    buffer.close()

    return StreamingResponse(
        buffer_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=payments.csv"}
    )
        


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.invoice import Invoice
from app.models.order import Order
from app.schemas.invoice import InvoiceCallback, InvoiceResponse

router = APIRouter(prefix="/invoice", tags=["Invoices"])

@router.post("/callback", response_model=InvoiceResponse)
def invoice_callback(data: InvoiceCallback, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {data.order_id} not found")
    
    invoice = Invoice(
        order_id=data.order_id,
        invoice_file_url=data.invoice_file_url,
        status='generated',
        extracted_data=data.extracted_data
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/{order_id}", response_model=InvoiceResponse)
def get_invoice(order_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail=f"No invoice found for order {order_id}")
    return invoice

import json
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.services.fraud import detect_fraud
from app.services.n8n import trigger_n8n

router = APIRouter(prefix="/order", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    total_price: float = Form(...),
    image: Optional[UploadFile] = File(None),
    invoice_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        image_path = f"uploads/products/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())

    db_order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price,
        uploaded_image_url=image_path,
        status='processing'
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    from app.workflows.langgraph_flow import run_flow
    
    extracted_text = None
    if invoice_file:
        from app.services.invoice_nlp import extract_text_from_pdf, extract_text_from_image
        os.makedirs('uploads/invoices', exist_ok=True)
        invoice_path = f"uploads/invoices/{invoice_file.filename}"
        with open(invoice_path, "wb") as f:
            f.write(await invoice_file.read())
        
        ext = invoice_file.filename.split('.')[-1].lower()
        if ext == 'pdf':
            extracted_text = extract_text_from_pdf(invoice_path)
        elif ext in ('jpg', 'jpeg', 'png'):
            extracted_text = extract_text_from_image(invoice_path)

    initial_state = {
        'order_id': db_order.id,
        'user_id': user_id,
        'product_id': product_id,
        'quantity': quantity,
        'total_price': total_price,
        'image_path': image_path,
        'invoice_text': extracted_text
    }

    final_state = run_flow(initial_state)

    fraud = final_state.get('fraud', False)
    decision = final_state.get('decision', 'flagged')
    n8n_triggered = final_state.get('n8n_triggered', False)

    db_order.is_fraud = fraud
    db_order.decision = decision
    db_order.status = decision
    db_order.nlp_summary = final_state.get('rag_context', '')

    db.commit()
    db.refresh(db_order)

    return OrderResponse(
        order_id=db_order.id,
        status=decision,
        fraud=fraud,
        image_analysis={'report': final_state.get('image_report', '')},
        invoice_data={'report': final_state.get('invoice_report', '')},
        decision=decision,
        n8n_triggered=n8n_triggered
    )

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

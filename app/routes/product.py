from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.product import Product

router = APIRouter()

@router.post('/add-product')
def add_product(name: str, price: float, db: Session = Depends(get_db)):
    product = Product(name=name, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

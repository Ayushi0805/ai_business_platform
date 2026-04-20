from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean
from app.db.database import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    uploaded_image_url = Column(String)
    status = Column(String, default='pending')
    is_fraud = Column(Boolean, default=False)
    image_analysis_result = Column(String, nullable=True)
    nlp_summary = Column(String, nullable=True)
    decision = Column(String, nullable=True)

from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    invoice_file_url = Column(String)
    status = Column(String, default='uploaded')
    extracted_data = Column(String, nullable=True)

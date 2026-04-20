from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, UploadFile, File
from app.db.database import engine, Base
from app.models import product, order, invoice
from app.routes import product as product_router
from app.routes import order as order_router_module
from app.routes import invoice as invoice_router_module

# The disassembly shows:
# IMPORT_FROM order -> STORE_NAME order_router
# IMPORT_FROM invoice -> STORE_NAME invoice_router
order_router = order_router_module 
invoice_router = invoice_router_module

app = FastAPI(
    title='AI Business Platform',
    description='Full-stack AI platform: FastAPI + LangGraph + CrewAI + LangChain + n8n',
    version='1.0.0'
)

Base.metadata.create_all(bind=engine)

app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(invoice_router.router)

@app.get('/', tags=['Health'])
def root():
    return {
        'message': 'AI Business Platform is running.',
        'docs': '/docs',
        'flow': 'FastAPI → LangGraph → CrewAI → LangChain → LLM → n8n'
    }

@app.post('/upload-image/', tags=['Uploads'])
async def upload_image(file: UploadFile = File(...)):
    import os
    os.makedirs('uploads/products', exist_ok=True)
    file_path = f"uploads/products/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    return {'file_path': file_path}

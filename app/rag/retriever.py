import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.rag.loader import load_and_split_documents

FAISS_INDEX_PATH = 'ml_models/faiss_index'
_retriever = None
_embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def get_retriever():
    global _retriever
    if _retriever is not None:
        return _retriever
    
    if os.path.exists(FAISS_INDEX_PATH):
        print('[RAG] Loading existing FAISS index...')
        vectorstore = FAISS.load_local(FAISS_INDEX_PATH, _embeddings, allow_dangerous_deserialization=True)
    else:
        print('[RAG] Building new FAISS index...')
        chunks = load_and_split_documents()
        if not chunks:
            print('[RAG] No documents found to index.')
            return None
        
        vectorstore = FAISS.from_documents(chunks, _embeddings)
        os.makedirs('ml_models', exist_ok=True)
        vectorstore.save_local(FAISS_INDEX_PATH)
        print('[RAG] FAISS index saved.')
    
    _retriever = vectorstore.as_retriever(search_kwargs={'k': 2})
    return _retriever

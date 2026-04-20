import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

DATA_DIR = 'data/knowledge_base'

def load_and_split_documents() -> list:
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, 'dummy_policy.txt'), 'w') as f:
            f.write('All orders above $10,000 must be manually reviewed unless the user is a VIP.\n')
            f.write('Laptops are high-risk items and require strict invoice validation.')

    loader = DirectoryLoader(DATA_DIR, glob='**/*.txt', loader_cls=TextLoader)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(docs)
    return chunks

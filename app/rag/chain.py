from app.rag.retriever import get_retriever

def query_rag(query: str) -> str:
    retriever = get_retriever()
    if not retriever:
        return 'No knowledge base documents available.'
    
    docs = retriever.invoke(query)
    if not docs:
        return 'No relevant context found.'
    
    context = '\n\n'.join([doc.page_content for doc in docs])
    return context

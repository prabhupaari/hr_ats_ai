import os
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from rag.embedder import get_openai_embedder

VECTOR_DB_DIR = "vector_db"

def create_or_load_vector_store(docs):
    embedder = get_openai_embedder()
    if os.path.exists(VECTOR_DB_DIR):
        store = FAISS.load_local(VECTOR_DB_DIR, embedder, allow_dangerous_deserialization=True)
        store.add_documents(docs)
        return store
    return FAISS.from_documents(docs, embedder)

def save_documents_to_vectorstore(docs: list[Document]):
    embedder = get_openai_embedder()
    store = create_or_load_vector_store(docs)
    #store.add_documents(docs)
    store.save_local(VECTOR_DB_DIR)

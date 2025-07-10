import json
from langchain.docstore.document import Document
from rag.vector_store import save_documents_to_vectorstore
from api.database import SessionLocal
from api.models import JobDescription as JD, Resume


def flatten_dict(data: dict, parent_key='', sep='.') -> dict:
    """Flatten nested dicts with dot notation (e.g., contact.name)."""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v)))
    return dict(items)

def index_resumes_to_faiss(parsed_data, resume):
    docs = []
    try:
        parsed_json = json.loads(parsed_data)
        if isinstance(parsed_json, str):
            parsed_json = json.loads(parsed_json)
        print(parsed_json)
        flattened = flatten_dict(parsed_json)
        print(flattened)
        content = "\n".join(f"{k}: {v}" for k, v in flattened.items())
        doc = Document(
            page_content=content,
            metadata={"type": "resume", "id": resume.id, "filename": resume.filename}
        )
        docs.append(doc)
    except Exception as e:
        print(f"❌ Failed to parse resume ID {resume.id}: {e}")

    save_documents_to_vectorstore(docs)
    print(f"✅ Indexed {len(docs)} parsed resumes into vector DB")

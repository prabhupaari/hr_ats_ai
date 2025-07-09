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

def index_resumes_to_faiss():
    db = SessionLocal()
    resumes = db.query(Resume).filter(Resume.is_parsed == True).all()

    docs = []
    for r in resumes:
        if r.parsed and r.parsed.parsed_data:
            try:
                parsed_json = json.loads(r.parsed.parsed_data)
                if isinstance(parsed_json, str):
                    parsed_json = json.loads(parsed_json)
                print(parsed_json)
                flattened = flatten_dict(parsed_json)
                print(flattened)
                content = "\n".join(f"{k}: {v}" for k, v in flattened.items())
                doc = Document(
                    page_content=content,
                    metadata={"type": "resume", "id": r.id, "filename": r.filename}
                )
                docs.append(doc)
            except Exception as e:
                print(f"❌ Failed to parse resume ID {r.id}: {e}")

    save_documents_to_vectorstore(docs)
    print(f"✅ Indexed {len(docs)} parsed resumes into vector DB")
    db.close()


# def index_jds_to_faiss():
#     db = SessionLocal()
#     jds = db.query(JD).all()

#     docs = []
#     for jd in jds:
#         docs.append(Document(
#             page_content=jd.description,
#             metadata={"type": "jd", "id": jd.id, "title": jd.title}
#         ))

#     save_documents_to_vectorstore(docs)
#     print(f"✅ Indexed {len(docs)} JDs into vector DB")
#     db.close()

# index_resumes_to_faiss()
# index_jds_to_faiss()
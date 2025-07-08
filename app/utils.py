import os
import fitz
from fastapi import UploadFile
from docx import Document


UPLOAD_DIR = "app/data/resumes"

def extract_text(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    text = ""
    if file.filename.endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    elif file.filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    elif file.filename.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")
    
    return text
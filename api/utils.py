import os
import json
import fitz
import openai
from fastapi import UploadFile
from docx import Document
from api.database import get_db
from api.models import Resume, ParsedResume
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


UPLOAD_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../data/resumes"))


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


def parse_resume_with_gpt(resume_text: str):
    prompt = f"""
        You are a resume parser. Extract the following fields in JSON:
        - Name
        - Email
        - Phone
        - Skills
        - Years of Experience
        - Current Designation
        - Education (Degree, University, Year)
        - Previous Companies with Role and Duration

        Resume Text:
        \"\"\"
        {resume_text}
        \"\"\"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def parse_and_save_resume(resume_id: int):
    db = next(get_db())  # create a new DB session
    try:
        resume = db.query(Resume).get(resume_id)
        if resume and not resume.is_parsed:
            parsed_data = parse_resume_with_gpt(resume.content)
            parsed_resume = ParsedResume(
                resume_id=resume.id,
                parsed_data=json.dumps(parsed_data)
            )
            db.add(parsed_resume)
            resume.is_parsed = True
            db.commit()
    except Exception as e:
        print(f"Error parsing resume {resume_id}: {e}")
    finally:
        db.close()

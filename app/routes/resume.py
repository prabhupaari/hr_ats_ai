import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Resume
from app.database import get_db
from app.utils import extract_text

router = APIRouter()
UPLOAD_DIR = "app/data/resumes"

@router.post("/")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    text = extract_text(file)
    
    resume = Resume(filename=file.filename, content=text)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {
        "filename": resume.filename,
        "id": resume.id,
        "created_at": resume.created_at
    }
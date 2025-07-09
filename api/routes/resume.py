import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from api.models import Resume
from api.database import get_db
from api.utils import extract_text, parse_and_save_resume

router = APIRouter()


@router.post("/")
async def upload_resume(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, db: Session = Depends(get_db)):
    text = extract_text(file)

    resume = Resume(filename=file.filename, content=text)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    #background_tasks.add_task(parse_and_save_resume, resume.id)

    return {
        "filename": resume.filename,
        "id": resume.id,
        "created_at": resume.created_at
    }

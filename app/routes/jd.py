from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import JDCreate, JDOut
from app.models import JobDescription
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=JDOut)
def upload_jd(jd: JDCreate, db: Session = Depends(get_db)):
    jd_obj = JobDescription(**jd.dict())
    db.add(jd_obj)
    db.commit()
    db.refresh(jd_obj)
    return jd_obj

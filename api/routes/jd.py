from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas import JDCreate, JDOut
from api.models import JobDescription
from api.database import get_db

router = APIRouter()


@router.post("/", response_model=JDOut)
def upload_jd(jd: JDCreate, db: Session = Depends(get_db)):
    jd_obj = JobDescription(**jd.dict())
    db.add(jd_obj)
    db.commit()
    db.refresh(jd_obj)
    return jd_obj

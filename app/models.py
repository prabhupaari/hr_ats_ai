from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
    is_parsed = Column(Boolean, default=False)
    parsed = relationship("ParsedResume", back_populates="resume", uselist=False)

class ParsedResume(Base):
    __tablename__ = "parsed_resumes"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    parsed_data = Column(Text)  # Store JSON string
    parsed_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="parsed")
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.dialects.sqlite import JSON
from .db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    salary_min = Column(Integer)
    post_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100))
    ghost_score = Column(Float)
    ghost_reason = Column(Text)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    resume_text = Column(Text)
    skills_json = Column(JSON)
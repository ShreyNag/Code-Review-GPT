from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    code_snippet = Column(Text, nullable=False)
    ai_feedback = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
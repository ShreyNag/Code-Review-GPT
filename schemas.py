from pydantic import BaseModel
from datetime import datetime

class CodeSubmission(BaseModel):
    code: str

class CodeReviewResponse(BaseModel):
    id: int
    code_snippet: str
    ai_feedback: str
    created_at: datetime

    class Config:
        from_attributes = True
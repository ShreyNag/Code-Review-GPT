import os
import sys
from typing import List

# 1. Ensure local imports work by adding the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import google.generativeai as genai
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# 2. Local module imports for database and schemas
from database import init_db, get_db
from models import CodeReview
from schemas import CodeSubmission, CodeReviewResponse

# Load environment variables (API Key and DB URL)
load_dotenv()

app = FastAPI(title="Code-Review-GPT")

# 3. Initialize PostgreSQL tables on startup
init_db()

# 4. Configure Gemini AI with the exact preview model found in your environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = 'models/gemini-3-flash-preview'

@app.post("/review", response_model=CodeReviewResponse)
async def create_code_review(submission: CodeSubmission, db: Session = Depends(get_db)):
    """
    Sends code to Gemini 3 Flash, saves review to PostgreSQL, and returns feedback.
    """
    prompt = (
        "You are an expert software engineer. Provide a detailed code review for this "
        "Python snippet, focusing on logic, security, and efficiency:\n\n"
        f"{submission.code}"
    )
    
    try:
        # Generate content using the Gemini 3 preview model
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="AI response was empty.")
            
        feedback = response.text

        # Save the result into your PostgreSQL database
        new_review = CodeReview(
            code_snippet=submission.code,
            ai_feedback=feedback
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        
        return new_review

    except Exception as e:
        if db:
            db.rollback()
        print(f"Detailed Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=List[CodeReviewResponse])
async def get_review_history(db: Session = Depends(get_db)):
    """
    Fetches all past reviews from PostgreSQL, sorted by date.
    """
    return db.query(CodeReview).order_by(CodeReview.created_at.desc()).all()

# --- 5. Serving the Web Interface ---

# Mount the 'static' folder so your browser can load index.html, CSS, and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    """
    Serves your frontend when you visit http://127.0.0.1:8000
    """
    return FileResponse('static/index.html')


@app.delete("/delete/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    """
    Finds a review by ID in PostgreSQL and deletes it permanently.
    """
    # 1. Look for the review in the database
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    
    # 2. If it doesn't exist, tell the user
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # 3. If found, delete it and save changes
    db.delete(review)
    db.commit()
    
    return {"message": f"Successfully deleted review {review_id}"}


from fpdf import FPDF
from fastapi.responses import Response

@app.get("/download/{review_id}")
async def download_pdf(review_id: int, db: Session = Depends(get_db)):
    # 1. Fetch the specific review from PostgreSQL
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # 2. Initialize PDF document
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Code Review Report #{review.id}", ln=True, align='C')
    pdf.ln(10)

    # Original Code Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Original Code Snippet:", ln=True)
    pdf.set_font("Courier", size=10) # Using Courier for code look
    pdf.multi_cell(0, 8, txt=review.code_snippet)
    pdf.ln(10)

    # AI Feedback Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="AI Feedback & Suggestions:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=review.ai_feedback)

    # 3. Generate PDF and return it as a downloadable response
    # 'dest=S' outputs the document as a string in memory
    pdf_output = pdf.output(dest='S').encode('latin-1', 'replace') 
    
    return Response(
        content=pdf_output, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=review_{review_id}.pdf"}
    )
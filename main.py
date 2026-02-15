"""
main.py - WITH ERROR LOGGING
─────────────────────────────────────────────
Full error details Terminal এ দেখাবে
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models
import traceback

from cv_extractor import process_cv_file
from crud import save_candidate_to_db, get_candidate_by_email, get_all_candidates
from schemas import CandidateResponse

app = FastAPI(
    title="CV Matching System",
    description="CV upload → Data save to pgAdmin4",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "CV Matching System running ✅",
        "docs": "http://localhost:8082/docs"
    }


@app.post("/upload-cv", response_model=CandidateResponse)
async def upload_cv(
    file: UploadFile = File(..., description="PDF বা DOCX CV file"),
    db: Session = Depends(get_db)
):
    """CV Upload করলে parse হবে এবং DB তে save হবে"""

    # ── File type check ────────────────────────────────────
    filename = file.filename
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="শুধু .pdf বা .docx file upload করুন"
        )

    print(f"\n📁 File received: {filename}")

    # ── File content পড়া ──────────────────────────────────
    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File empty!")

    # ── Text extract + Parse ───────────────────────────────
    try:
        print("🔍 CV processing started...")
        raw_text, extracted_data = process_cv_file(filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ CV processing error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"CV process করতে সমস্যা হয়েছে: {str(e)}"
        )

    # ── Duplicate email check ──────────────────────────────
    if extracted_data.email:
        existing = get_candidate_by_email(db, extracted_data.email)
        if existing:
            print(f"⚠️ Duplicate email found: {extracted_data.email}")
            raise HTTPException(
                status_code=409,
                detail=f"এই email দিয়ে আগেই CV জমা আছে: {extracted_data.email}"
            )

    # ── Database এ save করা ───────────────────────────────
    try:
        print("💾 Saving to database...")
        saved_candidate = save_candidate_to_db(db, extracted_data, raw_text)
        print(f"🎉 Successfully saved! ID: {saved_candidate.id}")
    except Exception as e:
        db.rollback()
        print(f"\n❌ DATABASE SAVE ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\n" + "="*60)
        
        raise HTTPException(
            status_code=500,
            detail=f"Database এ save করতে সমস্যা: {str(e)}"
        )

    # ── Success response ───────────────────────────────────
    return CandidateResponse(
        success      = True,
        candidate_id = saved_candidate.id,
        name         = saved_candidate.name,
        message      = f"✅ CV সফলভাবে save হয়েছে! Candidate ID: {saved_candidate.id}"
    )


@app.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):
    """সব candidate list"""
    candidates = get_all_candidates(db)

    result = []
    for c in candidates:
        result.append({
            "id":         c.id,
            "name":       c.name,
            "email":      c.email,
            "phone":      c.phone,
            "total_exp":  c.total_exp,
            "skills":     [s.skill_name for s in c.skills],
            "education":  [{"degree": e.degree, "institution": e.institution} for e in c.education],
            "experience": [{"company": ex.company, "role": ex.role} for ex in c.experience],
            "created_at": str(c.created_at)
        })

    return {
        "total": len(result),
        "candidates": result
    }


@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """নির্দিষ্ট candidate এর details"""
    from models import Candidate
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate পাওয়া যায়নি")

    return {
        "id":         candidate.id,
        "name":       candidate.name,
        "email":      candidate.email,
        "phone":      candidate.phone,
        "total_exp":  float(candidate.total_exp) if candidate.total_exp else None,
        "skills":     [s.skill_name for s in candidate.skills],
        "education": [
            {
                "degree":      e.degree,
                "institution": e.institution,
                "year":        e.year
            } for e in candidate.education
        ],
        "experience": [
            {
                "company":  ex.company,
                "role":     ex.role,
                "duration": ex.duration
            } for ex in candidate.experience
        ]
    }
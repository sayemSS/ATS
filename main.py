"""
main.py (UPDATED with Job Posting & Matching)
─────────────────────────────────────────────
CV upload + Job posting + CV-Job matching
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models

from cv_extractor import process_cv_file
from crud import save_candidate_to_db, get_candidate_by_email, get_all_candidates
from crud_jobs import create_job, get_all_jobs, get_job_by_id, match_candidates_to_job, get_match_results
from schemas import CandidateResponse, JobCreate, JobResponse, JobDetail, MatchResponse, MatchedCandidate

# ─────────────────────────────────────────────
# App তৈরি
# ─────────────────────────────────────────────
app = FastAPI(
    title="CV-Job Matching System",
    description="CV upload + Job posting + Intelligent matching",
    version="2.0.0"
)

Base.metadata.create_all(bind=engine)


# ═══════════════════════════════════════════════════════════
# GENERAL ROUTES
# ═══════════════════════════════════════════════════════════

@app.get("/")
def home():
    return {
        "message": "CV-Job Matching System running ✅",
        "endpoints": {
            "docs": "/docs",
            "upload_cv": "/upload-cv",
            "post_job": "/post-job",
            "match": "/match/{job_id}",
            "jobs": "/jobs",
            "candidates": "/candidates"
        }
    }


# ═══════════════════════════════════════════════════════════
# CV ROUTES (Already exists)
# ═══════════════════════════════════════════════════════════

@app.post("/upload-cv", response_model=CandidateResponse)
async def upload_cv(
    file: UploadFile = File(..., description="PDF বা DOCX CV file"),
    db: Session = Depends(get_db)
):
    """CV Upload করো → Database এ save হবে"""
    
    # File type check
    filename = file.filename
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="শুধু .pdf বা .docx file upload করুন")

    # File read
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File empty!")

    # Extract data
    try:
        raw_text, extracted_data = process_cv_file(filename, file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV process error: {str(e)}")

    # Duplicate check
    if extracted_data.email:
        existing = get_candidate_by_email(db, extracted_data.email)
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"এই email দিয়ে আগেই CV আছে: {extracted_data.email}"
            )

    # Save to database
    try:
        print("💾 Saving to database...")
        saved_candidate = save_candidate_to_db(db, extracted_data, raw_text)
    except Exception as e:
        db.rollback()
        print(f"❌ DATABASE SAVE ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        print("="*60)
        raise HTTPException(status_code=500, detail=f"Database save error: {str(e)}")

    return CandidateResponse(
        success      = True,
        candidate_id = saved_candidate.id,
        name         = saved_candidate.name,
        message      = f"✅ CV saved! Candidate ID: {saved_candidate.id}"
    )


@app.get("/candidates")
def list_candidates(db: Session = Depends(get_db)):
    """সব candidates list"""
    candidates = get_all_candidates(db)
    
    result = []
    for c in candidates:
        result.append({
            "id":         c.id,
            "name":       c.name,
            "email":      c.email,
            "total_exp":  float(c.total_exp) if c.total_exp else None,
            "skills":     [s.skill_name for s in c.skills],
            "created_at": str(c.created_at)
        })
    
    return {"total": len(result), "candidates": result}


# ═══════════════════════════════════════════════════════════
# JOB POSTING ROUTES (NEW)
# ═══════════════════════════════════════════════════════════

@app.post("/post-job", response_model=JobResponse)
def post_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """
    HR job post করবে।
    
    Example request body:
    {
        "title": "Senior Python Developer",
        "description": "We need a Python developer...",
        "min_experience": 3.0,
        "required_skills": ["Python", "Django", "REST API", "PostgreSQL"],
        "posted_by": "HR Team"
    }
    """
    
    try:
        print(f"\n📋 Creating job: {job_data.title}")
        job = create_job(db, job_data)
        
        return JobResponse(
            success = True,
            job_id  = job.id,
            title   = job.title,
            message = f"✅ Job posted successfully! ID: {job.id}"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Job post error: {str(e)}")


@app.get("/jobs", response_model=list[JobDetail])
def list_jobs(
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    সব jobs list।
    
    Query params:
    - status: "active" বা "closed" (optional)
    """
    
    jobs = get_all_jobs(db, status=status)
    
    result = []
    for job in jobs:
        result.append(JobDetail(
            id              = job.id,
            title           = job.title,
            description     = job.description,
            min_experience  = float(job.min_experience) if job.min_experience else None,
            required_skills = [s.skill_name for s in job.required_skills],
            posted_by       = job.posted_by,
            status          = job.status,
            created_at      = str(job.created_at)
        ))
    
    return result


@app.get("/jobs/{job_id}", response_model=JobDetail)
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    """নির্দিষ্ট job এর details"""
    
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobDetail(
        id              = job.id,
        title           = job.title,
        description     = job.description,
        min_experience  = float(job.min_experience) if job.min_experience else None,
        required_skills = [s.skill_name for s in job.required_skills],
        posted_by       = job.posted_by,
        status          = job.status,
        created_at      = str(job.created_at)
    )


# ═══════════════════════════════════════════════════════════
# MATCHING ROUTES (NEW)
# ═══════════════════════════════════════════════════════════

@app.post("/match/{job_id}", response_model=MatchResponse)
def match_job_with_candidates(job_id: int, db: Session = Depends(get_db)):
    """
    একটা job এর জন্য সব candidates match করো।
    Match scores calculate করে database এ save করে।
    """
    
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Matching করো
        matched_candidates = match_candidates_to_job(db, job_id)
        
        # Response তৈরি করো
        matches = [MatchedCandidate(**c) for c in matched_candidates]
        
        return MatchResponse(
            job_id           = job_id,
            job_title        = job.title,
            total_candidates = len(matches),
            matches          = matches
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")


@app.get("/match/{job_id}", response_model=MatchResponse)
def get_job_matches(job_id: int, db: Session = Depends(get_db)):
    """
    একটা job এর জন্য saved match results দেখাও।
    আগে match করা থাকতে হবে।
    """
    
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Saved match results নাও
    match_results = get_match_results(db, job_id)
    
    if not match_results:
        raise HTTPException(
            status_code=404,
            detail="No matches found. Use POST /match/{job_id} to calculate matches first."
        )
    
    # Format করো
    matches = []
    for match in match_results:
        candidate = match.candidate
        
        matches.append(MatchedCandidate(
            candidate_id   = candidate.id,
            name           = candidate.name,
            email          = candidate.email,
            phone          = candidate.phone,
            total_exp      = float(candidate.total_exp) if candidate.total_exp else None,
            match_score    = float(match.match_score),
            matched_skills = match.matched_skills.split(', ') if match.matched_skills else [],
            missing_skills = []  # এটা calculate করতে হবে
        ))
    
    return MatchResponse(
        job_id           = job_id,
        job_title        = job.title,
        total_candidates = len(matches),
        matches          = matches
    )

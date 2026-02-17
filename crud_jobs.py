"""
crud_jobs.py
─────────────────────────────────────────────
Job posting এবং CV-Job matching operations
"""

from sqlalchemy.orm import Session
from models import Job, JobRequiredSkill, MatchResult, Candidate, CandidateSkill
from schemas import JobCreate


# ═══════════════════════════════════════════════════════════
# JOB OPERATIONS
# ═══════════════════════════════════════════════════════════

def create_job(db: Session, job_data: JobCreate) -> Job:
    """
    HR job post করবে।
    
    Flow:
    1. jobs table এ main info save
    2. job_required_skills table এ skills save
    """
    
    # Step 1: Main job info save করো
    db_job = Job(
        title          = job_data.title,
        description    = job_data.description,
        min_experience = job_data.min_experience,
        posted_by      = job_data.posted_by,
        status         = 'active'
    )
    db.add(db_job)
    db.flush()  # job_id পাও
    
    job_id = db_job.id
    print(f"✅ Job posted: ID={job_id}, Title={job_data.title}")
    
    # Step 2: Required skills save করো
    if job_data.required_skills:
        for skill in job_data.required_skills:
            if skill and skill.strip():
                db_skill = JobRequiredSkill(
                    job_id     = job_id,
                    skill_name = skill.strip()
                )
                db.add(db_skill)
        print(f"✅ Required skills saved: {job_data.required_skills}")
    
    db.commit()
    db.refresh(db_job)
    
    return db_job


def get_job_by_id(db: Session, job_id: int) -> Job:
    """Job ID দিয়ে job খোঁজা"""
    return db.query(Job).filter(Job.id == job_id).first()


def get_all_jobs(db: Session, status: str = None) -> list[Job]:
    """
    সব jobs list।
    status দিলে সেই status এর job (active/closed)
    """
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    return query.order_by(Job.created_at.desc()).all()


# ═══════════════════════════════════════════════════════════
# CV-JOB MATCHING
# ═══════════════════════════════════════════════════════════

def calculate_match_score(
    candidate_skills: list[str],
    required_skills: list[str]
) -> tuple[float, list[str], list[str]]:
    """
    Matching score calculate করে।
    
    Returns:
        (match_score, matched_skills, missing_skills)
    
    Example:
        Candidate: ["Python", "Django", "PostgreSQL"]
        Required:  ["Python", "Django", "REST API"]
        
        Matched: ["Python", "Django"]  → 2 out of 3 = 66.67%
        Missing: ["REST API"]
    """
    if not required_skills:
        return 100.0, [], []
    
    # Case-insensitive comparison
    candidate_skills_lower = [s.lower() for s in candidate_skills if s]
    required_skills_lower  = [s.lower() for s in required_skills if s]
    
    # Match করা skills খুঁজো
    matched = []
    for req_skill in required_skills:
        if req_skill.lower() in candidate_skills_lower:
            matched.append(req_skill)
    
    # Missing skills
    missing = [s for s in required_skills if s.lower() not in candidate_skills_lower]
    
    # Score calculate করো (percentage)
    match_score = (len(matched) / len(required_skills)) * 100
    
    return round(match_score, 2), matched, missing


def match_candidates_to_job(db: Session, job_id: int) -> list[dict]:
    """
    একটা job এর জন্য সব candidates match করে।
    
    Returns:
        List of matched candidates with scores
    """
    
    # Job খুঁজো
    job = get_job_by_id(db, job_id)
    if not job:
        return []
    
    # Job এর required skills
    required_skills = [s.skill_name for s in job.required_skills]
    
    print(f"\n🔍 Matching candidates for job: {job.title}")
    print(f"   Required skills: {required_skills}")
    
    # সব candidates নাও
    candidates = db.query(Candidate).all()
    
    matched_candidates = []
    
    for candidate in candidates:
        # Candidate এর skills
        candidate_skills = [s.skill_name for s in candidate.skills]
        
        # Match score calculate করো
        match_score, matched_skills, missing_skills = calculate_match_score(
            candidate_skills,
            required_skills
        )
        
        # Minimum score filter (optional)
        # যদি চাও তাহলে শুধু 50%+ match show করবে
        # if match_score < 50:
        #     continue
        
        # Match result save করো database এ
        # Check করো আগেই save করা আছে কিনা
        existing_match = db.query(MatchResult).filter(
            MatchResult.candidate_id == candidate.id,
            MatchResult.job_id == job_id
        ).first()
        
        if existing_match:
            # Update করো
            existing_match.match_score = match_score
            existing_match.matched_skills = ', '.join(matched_skills)
        else:
            # নতুন করে save করো
            match_result = MatchResult(
                candidate_id   = candidate.id,
                job_id         = job_id,
                match_score    = match_score,
                matched_skills = ', '.join(matched_skills)
            )
            db.add(match_result)
        
        # Response এর জন্য data তৈরি করো
        matched_candidates.append({
            'candidate_id':   candidate.id,
            'name':           candidate.name,
            'email':          candidate.email,
            'phone':          candidate.phone,
            'total_exp':      float(candidate.total_exp) if candidate.total_exp else None,
            'match_score':    match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills
        })
    
    db.commit()
    
    # Sort by match score (highest first)
    matched_candidates.sort(key=lambda x: x['match_score'], reverse=True)
    
    print(f"✅ Found {len(matched_candidates)} matching candidates")
    
    return matched_candidates


def get_match_results(db: Session, job_id: int) -> list[MatchResult]:
    """
    একটা job এর জন্য saved match results।
    Database থেকে পড়ে নেয়।
    """
    return db.query(MatchResult).filter(
        MatchResult.job_id == job_id
    ).order_by(
        MatchResult.match_score.desc()
    ).all()

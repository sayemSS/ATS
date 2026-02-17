"""
schemas.py (UPDATED with Job schemas)
─────────────────────────────────────────────
CV schemas + Job schemas
"""

from pydantic import BaseModel
from typing import List, Optional


# ═══════════════════════════════════════════════════════════
# CANDIDATE SCHEMAS (Already exists)
# ═══════════════════════════════════════════════════════════

class EducationItem(BaseModel):
    degree:      Optional[str] = None
    institution: Optional[str] = None
    year:        Optional[str] = None


class ExperienceItem(BaseModel):
    company:  Optional[str] = None
    role:     Optional[str] = None
    duration: Optional[str] = None


class CVExtractedData(BaseModel):
    name:        Optional[str]                  = None
    email:       Optional[str]                  = None
    phone:       Optional[str]                  = None
    total_exp:   Optional[float]                = None
    skills:      Optional[List[str]]            = []
    education:   Optional[List[EducationItem]]  = []
    experience:  Optional[List[ExperienceItem]] = []


class CandidateResponse(BaseModel):
    success:      bool
    candidate_id: int
    name:         Optional[str]
    message:      str

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════
# JOB SCHEMAS (NEW)
# ═══════════════════════════════════════════════════════════

class JobCreate(BaseModel):
    """HR job post করার সময় এই data দেবে"""
    title:           str
    description:     Optional[str] = None
    min_experience:  Optional[float] = None
    required_skills: List[str]               # যেমন: ["Python", "Django", "REST API"]
    posted_by:       Optional[str] = "HR"


class JobResponse(BaseModel):
    """Job post করার পর response"""
    success:    bool
    job_id:     int
    title:      str
    message:    str

    class Config:
        from_attributes = True


class JobDetail(BaseModel):
    """Job এর সব details"""
    id:              int
    title:           str
    description:     Optional[str]
    min_experience:  Optional[float]
    required_skills: List[str]
    posted_by:       Optional[str]
    status:          str
    created_at:      str

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════
# MATCHING SCHEMAS (NEW)
# ═══════════════════════════════════════════════════════════

class MatchedCandidate(BaseModel):
    """একজন matched candidate এর info"""
    candidate_id:    int
    name:            Optional[str]
    email:           Optional[str]
    phone:           Optional[str]
    total_exp:       Optional[float]
    match_score:     float                    # 0-100
    matched_skills:  List[str]                # যে skills match করেছে
    missing_skills:  List[str]                # যে skills নেই

    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    """Job এর জন্য সব matched candidates"""
    job_id:           int
    job_title:        str
    total_candidates: int
    matches:          List[MatchedCandidate]

    class Config:
        from_attributes = True

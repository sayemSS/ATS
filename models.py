"""
models.py (UPDATED with Job tables)
─────────────────────────────────────────────
CV tables + Job tables + Matching table
"""

from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ═══════════════════════════════════════════════════════════
# CANDIDATE TABLES (Already exists)
# ═══════════════════════════════════════════════════════════

class Candidate(Base):
    """TABLE 1: candidates"""
    __tablename__ = "candidates"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255))
    email       = Column(String(255), unique=True)
    phone       = Column(String(50))
    total_exp   = Column(Numeric(4, 1))
    raw_text    = Column(Text)
    created_at  = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    skills      = relationship("CandidateSkill",     back_populates="candidate", cascade="all, delete")
    education   = relationship("CandidateEducation", back_populates="candidate", cascade="all, delete")
    experience  = relationship("CandidateExperience",back_populates="candidate", cascade="all, delete")
    matches     = relationship("MatchResult",        back_populates="candidate", cascade="all, delete")


class CandidateSkill(Base):
    """TABLE 2: candidate_skills"""
    __tablename__ = "candidate_skills"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    skill_name      = Column(String(100))

    candidate       = relationship("Candidate", back_populates="skills")


class CandidateEducation(Base):
    """TABLE 3: candidate_education"""
    __tablename__ = "candidate_education"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    degree          = Column(String(255))
    institution     = Column(String(255))
    year            = Column(String(10))

    candidate       = relationship("Candidate", back_populates="education")


class CandidateExperience(Base):
    """TABLE 4: candidate_experience"""
    __tablename__ = "candidate_experience"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    company         = Column(String(255))
    role            = Column(String(255))
    duration        = Column(String(100))

    candidate       = relationship("Candidate", back_populates="experience")


# ═══════════════════════════════════════════════════════════
# JOB TABLES (NEW)
# ═══════════════════════════════════════════════════════════

class Job(Base):
    """TABLE 5: jobs - HR যে job post করে"""
    __tablename__ = "jobs"

    id              = Column(Integer, primary_key=True, index=True)
    title           = Column(String(255), nullable=False)
    description     = Column(Text)
    min_experience  = Column(Numeric(4, 1))
    posted_by       = Column(String(255))
    status          = Column(String(50), default='active')
    created_at      = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    required_skills = relationship("JobRequiredSkill", back_populates="job", cascade="all, delete")
    matches         = relationship("MatchResult",      back_populates="job", cascade="all, delete")


class JobRequiredSkill(Base):
    """TABLE 6: job_required_skills - Job এ কী skill দরকার"""
    __tablename__ = "job_required_skills"

    id              = Column(Integer, primary_key=True, index=True)
    job_id          = Column(Integer, ForeignKey("jobs.id"))
    skill_name      = Column(String(100), nullable=False)

    job             = relationship("Job", back_populates="required_skills")


class MatchResult(Base):
    """TABLE 7: match_results - CV-Job matching scores"""
    __tablename__ = "match_results"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    job_id          = Column(Integer, ForeignKey("jobs.id"))
    match_score     = Column(Numeric(5, 2))
    matched_skills  = Column(Text)
    created_at      = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    candidate       = relationship("Candidate", back_populates="matches")
    job             = relationship("Job",       back_populates="matches")

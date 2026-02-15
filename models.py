from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255))
    email       = Column(String(255), unique=True)
    phone       = Column(String(50))
    total_exp   = Column(Numeric(4, 1))  
    raw_text    = Column(Text)            
    created_at  = Column(TIMESTAMP, server_default=func.now())

    
    skills      = relationship("CandidateSkill",     back_populates="candidate", cascade="all, delete")
    education   = relationship("CandidateEducation", back_populates="candidate", cascade="all, delete")
    experience  = relationship("CandidateExperience",back_populates="candidate", cascade="all, delete")


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    skill_name      = Column(String(100))

    candidate       = relationship("Candidate", back_populates="skills")


class CandidateEducation(Base):
    __tablename__ = "candidate_education"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    degree          = Column(String(255))
    institution     = Column(String(255))
    year            = Column(String(10))

    candidate       = relationship("Candidate", back_populates="education")


class CandidateExperience(Base):
    __tablename__ = "candidate_experience"

    id              = Column(Integer, primary_key=True, index=True)
    candidate_id    = Column(Integer, ForeignKey("candidates.id"))
    company         = Column(String(255))
    role            = Column(String(255))
    duration        = Column(String(100))

    candidate       = relationship("Candidate", back_populates="experience")

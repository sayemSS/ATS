

from pydantic import BaseModel
from typing import List, Optional

class EducationItem(BaseModel):
    degree:      Optional[str] = None
    institution: Optional[str] = None
    year:        Optional[str] = None


class ExperienceItem(BaseModel):
    company:  Optional[str] = None
    role:     Optional[str] = None
    duration: Optional[str] = None


class CVExtractedData(BaseModel):

    name:        Optional[str]            = None
    email:       Optional[str]            = None
    phone:       Optional[str]            = None
    total_exp:   Optional[float]          = None     
    skills:      Optional[List[str]]      = []
    education:   Optional[List[EducationItem]]  = []
    experience:  Optional[List[ExperienceItem]] = []


class CandidateResponse(BaseModel):
    success:      bool
    candidate_id: int
    name:         Optional[str]
    message:      str

    class Config:
        from_attributes = True

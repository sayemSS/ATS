"""
crud.py
─────────────────────────────────────────────
CRUD = Create, Read, Update, Delete
এই file এর কাজ শুধু DB তে data save করা।
Business logic এখানে নেই — শুধু DB operations।
"""

from sqlalchemy.orm import Session
from models import Candidate, CandidateSkill, CandidateEducation, CandidateExperience
from schemas import CVExtractedData


def save_candidate_to_db(
    db: Session,
    extracted_data: CVExtractedData,
    raw_text: str
) -> Candidate:
    """
    Gemini থেকে পাওয়া extracted data গুলো
    আলাদা আলাদা table এ save করে।

    Flow:
    1. candidates table এ main info save → candidate_id পাই
    2. সেই candidate_id দিয়ে skills save
    3. সেই candidate_id দিয়ে education save
    4. সেই candidate_id দিয়ে experience save
    """

    # ── STEP 1: candidates table এ main info save ──────────
    db_candidate = Candidate(
        name      = extracted_data.name,
        email     = extracted_data.email,
        phone     = extracted_data.phone,
        total_exp = extracted_data.total_exp,
        raw_text  = raw_text          # CV এর পুরো text backup
    )
    db.add(db_candidate)
    db.flush()  # এখনই commit না করে শুধু candidate_id নাও
    # flush() করলে id পাওয়া যায় কিন্তু transaction এখনও open থাকে

    candidate_id = db_candidate.id
    print(f"✅ Candidate saved: ID={candidate_id}, Name={extracted_data.name}")


    # ── STEP 2: candidate_skills table এ skills save ───────
    if extracted_data.skills:
        for skill in extracted_data.skills:
            if skill and skill.strip():  # empty string check
                db_skill = CandidateSkill(
                    candidate_id = candidate_id,
                    skill_name   = skill.strip()
                )
                db.add(db_skill)
        print(f"✅ Skills saved: {extracted_data.skills}")


    # ── STEP 3: candidate_education table এ education save ─
    if extracted_data.education:
        for edu in extracted_data.education:
            if edu:
                db_edu = CandidateEducation(
                    candidate_id = candidate_id,
                    degree       = edu.degree,
                    institution  = edu.institution,
                    year         = edu.year
                )
                db.add(db_edu)
        print(f"✅ Education saved: {len(extracted_data.education)} entries")


    # ── STEP 4: candidate_experience table এ experience save
    if extracted_data.experience:
        for exp in extracted_data.experience:
            if exp:
                db_exp = CandidateExperience(
                    candidate_id = candidate_id,
                    company      = exp.company,
                    role         = exp.role,
                    duration     = exp.duration
                )
                db.add(db_exp)
        print(f"✅ Experience saved: {len(extracted_data.experience)} entries")


    # ── STEP 5: সব একসাথে DB তে commit ────────────────────
    db.commit()
    db.refresh(db_candidate)  # DB থেকে updated data নাও

    return db_candidate


def get_candidate_by_email(db: Session, email: str) -> Candidate:
    """Email দিয়ে candidate খোঁজা — duplicate check এর জন্য"""
    return db.query(Candidate).filter(Candidate.email == email).first()


def get_all_candidates(db: Session) -> list[Candidate]:
    """সব candidate এর list — Dashboard এ দেখানোর জন্য"""
    return db.query(Candidate).all()

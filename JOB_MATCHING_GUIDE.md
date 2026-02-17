# 🎯 JOB POSTING + CV-JOB MATCHING - Complete Guide

তোমার CV system এখন কাজ করছে! ✅

এখন **Job Posting এবং Matching** add করবো।

---

## 📋 কী কী হবে:

```
1. HR job post করবে (title, required skills, experience)
2. Job data database এ save হবে
3. সব CV candidates এর সাথে job match হবে
4. Match score (%) calculate হবে
5. Best candidates ranking-সহ দেখাবে
```

---

## 🚀 Implementation (Step by Step)

### Step 1: Database Tables তৈরি করো

**pgAdmin4** খোলো → `cv_matching_db` database select করো → Query Tool

**create_job_tables.sql** এর content copy করে paste করো এবং **F5** চাপো।

3টা নতুন table তৈরি হবে:
- `jobs` - HR যে job post করে
- `job_required_skills` - Job এ কী skill দরকার
- `match_results` - CV-Job matching scores

---

### Step 2: Files Replace করো

**এই 4টা file replace করতে হবে:**

| পুরনো File | নতুন File (আমি দিয়েছি) | Action |
|-------------|--------------------------|--------|
| `models.py` | `models_UPDATED.py` | Rename করে `models.py` বানাও |
| `schemas.py` | `schemas_UPDATED.py` | Rename করে `schemas.py` বানাও |
| `main.py` | `main_UPDATED.py` | Rename করে `main.py` বানাও |
| (নতুন) | `crud_jobs.py` | এমনিতেই রাখো |

**Command (Windows):**
```bash
# Backup করো
copy models.py models_old.py
copy schemas.py schemas_old.py
copy main.py main_old.py

# নতুন files replace করো
# Download করা files গুলো rename করে রাখো
```

---

### Step 3: Server Restart করো

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8082
```

---

## 📤 কিভাবে Use করবে:

### 1️⃣ Job Post করো (HR)

**POST /post-job**

Browser: `http://localhost:8082/docs` → `/post-job` → Try it out

Example Request:
```json
{
  "title": "Senior Python Developer",
  "description": "We need an experienced Python developer for our backend team.",
  "min_experience": 3.0,
  "required_skills": [
    "Python",
    "Django",
    "REST API",
    "PostgreSQL",
    "Docker"
  ],
  "posted_by": "HR Team"
}
```

Response:
```json
{
  "success": true,
  "job_id": 1,
  "title": "Senior Python Developer",
  "message": "✅ Job posted successfully! ID: 1"
}
```

---

### 2️⃣ Candidates Match করো

**POST /match/1** (যেখানে 1 হলো job_id)

Browser: `/match/1` → Try it out → Execute

Response:
```json
{
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "total_candidates": 3,
  "matches": [
    {
      "candidate_id": 1,
      "name": "AKASH KUMAR MIKON",
      "email": "kmakash56@gmail.com",
      "match_score": 80.0,
      "matched_skills": ["Python", "Django", "PostgreSQL", "Docker"],
      "missing_skills": ["REST API"]
    },
    {
      "candidate_id": 2,
      "name": "John Doe",
      "match_score": 60.0,
      "matched_skills": ["Python", "PostgreSQL", "Docker"],
      "missing_skills": ["Django", "REST API"]
    }
  ]
}
```

---

### 3️⃣ সব Jobs দেখো

**GET /jobs**

Response:
```json
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "...",
    "min_experience": 3.0,
    "required_skills": ["Python", "Django", "REST API", "PostgreSQL", "Docker"],
    "status": "active",
    "created_at": "2025-02-18..."
  }
]
```

---

### 4️⃣ Match Results দেখো (Database থেকে)

**GET /match/1**

এটা database এ saved match results দেখাবে।

---

## 🔍 Matching Logic কিভাবে কাজ করে:

```
Job Required Skills: ["Python", "Django", "REST API"]
Candidate Skills:    ["Python", "Django", "PostgreSQL"]

✅ Matched: Python, Django (2 out of 3)
❌ Missing: REST API

Match Score = (2 / 3) × 100 = 66.67%
```

---

## 📊 pgAdmin4 এ Data দেখো:

### Jobs:
```sql
SELECT * FROM jobs;
```

### Job Required Skills:
```sql
SELECT j.title, s.skill_name 
FROM jobs j 
JOIN job_required_skills s ON j.id = s.job_id;
```

### Match Results:
```sql
SELECT 
    c.name AS candidate,
    j.title AS job,
    m.match_score,
    m.matched_skills
FROM match_results m
JOIN candidates c ON m.candidate_id = c.id
JOIN jobs j ON m.job_id = j.id
ORDER BY m.match_score DESC;
```

---

## 🎯 Available Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-cv` | CV upload করো |
| POST | `/post-job` | Job post করো |
| POST | `/match/{job_id}` | Candidates match করো |
| GET | `/jobs` | সব jobs list |
| GET | `/jobs/{job_id}` | Job details |
| GET | `/match/{job_id}` | Match results দেখো |
| GET | `/candidates` | সব candidates list |

---

## 🎉 Final Test Workflow:

```
1. CV upload করো (যেমন 3-4টা CV)
   → POST /upload-cv

2. Job post করো
   → POST /post-job

3. Match calculate করো
   → POST /match/1

4. Results দেখো
   → GET /match/1

5. pgAdmin4 এ check করো
   → SELECT * FROM match_results;
```

---

## 💡 Future Enhancements (Optional):

- Email notification (matched candidates কে email পাঠাও)
- Experience-based filtering
- Education matching
- Weighted scoring (different skills different weights)
- Dashboard UI (React/Vue frontend)

---

এখন files replace করো এবং test করো! 🚀

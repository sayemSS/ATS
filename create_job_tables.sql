-- ================================
-- JOB POSTING TABLES
-- pgAdmin4 Query Tool এ run করো
-- ================================

-- TABLE 5: jobs (HR যে job post করবে)
CREATE TABLE IF NOT EXISTS jobs (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    min_experience  NUMERIC(4,1),           -- Minimum years required
    posted_by       VARCHAR(255),           -- HR name
    status          VARCHAR(50) DEFAULT 'active',  -- active/closed
    created_at      TIMESTAMP DEFAULT NOW()
);

-- TABLE 6: job_required_skills (Job এ কী skill দরকার)
CREATE TABLE IF NOT EXISTS job_required_skills (
    id              SERIAL PRIMARY KEY,
    job_id          INT REFERENCES jobs(id) ON DELETE CASCADE,
    skill_name      VARCHAR(100) NOT NULL
);

-- TABLE 7: match_results (CV-Job matching scores)
CREATE TABLE IF NOT EXISTS match_results (
    id              SERIAL PRIMARY KEY,
    candidate_id    INT REFERENCES candidates(id) ON DELETE CASCADE,
    job_id          INT REFERENCES jobs(id) ON DELETE CASCADE,
    match_score     NUMERIC(5,2),           -- Percentage (0-100)
    matched_skills  TEXT,                   -- Comma-separated matched skills
    created_at      TIMESTAMP DEFAULT NOW(),
    
    -- একই candidate একই job এ একবারই match হবে
    UNIQUE(candidate_id, job_id)
);

-- Success message
SELECT 'Job Tables তৈরি হয়ে গেছে! ✅' AS status;

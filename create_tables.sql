

-- TABLE 1: মূল candidate তথ্য
CREATE TABLE IF NOT EXISTS candidates (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255),
    email       VARCHAR(255) UNIQUE,
    phone       VARCHAR(50),
    total_exp   NUMERIC(4,1),          -- বছরে (যেমন 2.5)
    raw_text    TEXT,                  -- CV এর পুরো text backup
    created_at  TIMESTAMP DEFAULT NOW()
);

-- TABLE 2: candidate এর skills
CREATE TABLE IF NOT EXISTS candidate_skills (
    id              SERIAL PRIMARY KEY,
    candidate_id    INT REFERENCES candidates(id) ON DELETE CASCADE,
    skill_name      VARCHAR(100)
);

-- TABLE 3: candidate এর education
CREATE TABLE IF NOT EXISTS candidate_education (
    id              SERIAL PRIMARY KEY,
    candidate_id    INT REFERENCES candidates(id) ON DELETE CASCADE,
    degree          VARCHAR(255),
    institution     VARCHAR(255),
    year            VARCHAR(10)
);

-- TABLE 4: candidate এর work experience
CREATE TABLE IF NOT EXISTS candidate_experience (
    id              SERIAL PRIMARY KEY,
    candidate_id    INT REFERENCES candidates(id) ON DELETE CASCADE,
    company         VARCHAR(255),
    role            VARCHAR(255),
    duration        VARCHAR(100)        -- যেমন "2 years"
);

-- সব ঠিকঠাক হলে এই message দেখাবে
SELECT 'সব Table তৈরি হয়ে গেছে! ✅' AS status;

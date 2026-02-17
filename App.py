"""
app.py - CV-Job Matching System UI
Beautiful Streamlit Dashboard - Full English
"""

import streamlit as st
import requests

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
API_BASE_URL = "http://localhost:8082"

st.set_page_config(
    page_title="CV Matching System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS - Modern Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    .stApp {
        background-color: #0a0e1a;
        color: #e2e8f0;
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1525 0%, #111827 100%);
        border-right: 1px solid #1e2d4a;
    }

    .main-header {
        background: linear-gradient(135deg, #0d1525 0%, #162440 50%, #0d1525 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }

    .main-header h1 {
        font-family: 'Space Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }

    .main-header p {
        color: #64748b;
        font-size: 1rem;
        margin-top: 8px;
        font-weight: 300;
    }

    .metric-card {
        background: #111827;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 20px 24px;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
    }

    .metric-number {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #60a5fa;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .section-card {
        background: #111827;
        border: 1px solid #1e2d4a;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
    }

    .score-high {
        background: linear-gradient(135deg, #065f46, #047857);
        color: #34d399;
        border: 1px solid #059669;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .score-mid {
        background: linear-gradient(135deg, #78350f, #92400e);
        color: #fbbf24;
        border: 1px solid #d97706;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .score-low {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        color: #f87171;
        border: 1px solid #dc2626;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .skill-tag-green {
        background: rgba(52, 211, 153, 0.1);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 2px;
    }

    .skill-tag-red {
        background: rgba(248, 113, 113, 0.1);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 2px;
    }

    .skill-tag-blue {
        background: rgba(96, 165, 250, 0.1);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        display: inline-block;
        margin: 2px;
    }

    .candidate-card {
        background: #0d1525;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s;
    }

    .candidate-card:hover { border-color: #3b82f6; }

    .candidate-name {
        font-family: 'Space Mono', monospace;
        font-size: 1rem;
        color: #e2e8f0;
        font-weight: 700;
    }

    .candidate-info {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    .progress-bar-bg {
        background: #1e2d4a;
        border-radius: 999px;
        height: 8px;
        width: 100%;
        margin-top: 8px;
    }

    .bar-green {
        background: linear-gradient(90deg, #059669, #34d399);
        border-radius: 999px;
        height: 8px;
    }

    .bar-yellow {
        background: linear-gradient(90deg, #d97706, #fbbf24);
        border-radius: 999px;
        height: 8px;
    }

    .bar-red {
        background: linear-gradient(90deg, #dc2626, #f87171);
        border-radius: 999px;
        height: 8px;
    }

    .success-msg {
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #34d399;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 0.9rem;
        margin: 12px 0;
    }

    .error-msg {
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.3);
        color: #f87171;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 0.9rem;
        margin: 12px 0;
    }

    .custom-divider {
        border: none;
        border-top: 1px solid #1e2d4a;
        margin: 20px 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: #0d1525 !important;
        border: 1px solid #1e2d4a !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }

    .sidebar-logo {
        text-align: center;
        padding: 20px;
        border-bottom: 1px solid #1e2d4a;
        margin-bottom: 20px;
    }

    .sidebar-logo h2 {
        font-family: 'Space Mono', monospace;
        font-size: 1.2rem;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #34d399;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .job-card {
        background: #0d1525;
        border: 1px solid #1e2d4a;
        border-left: 3px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s;
    }

    .job-card:hover {
        border-color: #60a5fa;
        border-left-color: #60a5fa;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
    }

    .job-title {
        font-family: 'Space Mono', monospace;
        font-size: 1rem;
        color: #60a5fa;
        font-weight: 700;
    }

    .stSelectbox > div > div {
        background: #0d1525 !important;
        border: 1px solid #1e2d4a !important;
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API Helper Functions
# ─────────────────────────────────────────────

def api_get(endpoint):
    try:
        r = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        return (True, r.json()) if r.status_code == 200 else (False, r.json())
    except requests.exceptions.ConnectionError:
        return False, {"detail": "Cannot connect to server! Is the FastAPI server running?"}
    except Exception as e:
        return False, {"detail": str(e)}


def api_post(endpoint, data=None, files=None):
    try:
        if files:
            r = requests.post(f"{API_BASE_URL}{endpoint}", files=files, timeout=60)
        else:
            r = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=60)
        return (True, r.json()) if r.status_code == 200 else (False, r.json())
    except requests.exceptions.ConnectionError:
        return False, {"detail": "Cannot connect to server! Is the FastAPI server running?"}
    except Exception as e:
        return False, {"detail": str(e)}


def score_class(score):
    if score >= 70: return "score-high"
    if score >= 40: return "score-mid"
    return "score-low"


def bar_class(score):
    if score >= 70: return "bar-green"
    if score >= 40: return "bar-yellow"
    return "bar-red"


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🎯 CV MATCHER</h2>
        <p style="color: #64748b; font-size: 0.8rem;">AI-Powered Recruitment</p>
        <div style="margin-top: 8px;">
            <span class="status-dot"></span>
            <span style="color: #34d399; font-size: 0.8rem;">System Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "Navigation",
        ["🏠 Dashboard", "📄 Upload CV", "💼 Post Job", "🎯 Matching", "👥 Candidates", "📋 Jobs List"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Quick Stats**")

    ok1, d1 = api_get("/candidates")
    ok2, d2 = api_get("/jobs")

    total_cv   = d1.get("total", 0) if ok1 else 0
    total_jobs = len(d2) if ok2 and isinstance(d2, list) else 0

    c1, c2 = st.columns(2)
    with c1: st.metric("CVs", total_cv)
    with c2: st.metric("Jobs", total_jobs)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #374151; font-size: 0.75rem; text-align: center; padding: 12px;">
        API: localhost:8082 · v2.0
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Dashboard
# ─────────────────────────────────────────────
if page == "🏠 Dashboard":

    st.markdown("""
    <div class="main-header">
        <h1>CV – Job Matching System</h1>
        <p>AI-powered recruitment platform · Upload CVs · Post Jobs · Find Best Matches</p>
    </div>
    """, unsafe_allow_html=True)

    ok1, d1 = api_get("/candidates")
    ok2, d2 = api_get("/jobs")

    total_cv   = d1.get("total", 0) if ok1 else 0
    total_jobs = len(d2) if ok2 and isinstance(d2, list) else 0
    active     = len([j for j in d2 if j.get("status") == "active"]) if ok2 and isinstance(d2, list) else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{total_cv}</div><div class="metric-label">Total CVs</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{total_jobs}</div><div class="metric-label">Total Jobs</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{active}</div><div class="metric-label">Active Jobs</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-number">✓</div><div class="metric-label">System Online</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**👥 Recent Candidates**")

        if ok1 and d1.get("candidates"):
            for c in d1["candidates"][-5:][::-1]:
                skills_html = "".join([f'<span class="skill-tag-blue">{s}</span>' for s in (c.get("skills") or [])[:3]])
                st.markdown(f"""
                <div class="candidate-card">
                    <div class="candidate-name">#{c['id']} {c.get('name') or 'Unknown'}</div>
                    <div class="candidate-info">📧 {c.get('email') or 'N/A'}</div>
                    <div style="margin-top:8px">{skills_html}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-msg">No candidates found. Upload a CV first.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**💼 Active Jobs**")

        if ok2 and isinstance(d2, list) and len(d2) > 0:
            for job in d2[-5:][::-1]:
                skills_html = "".join([f'<span class="skill-tag-green">{s}</span>' for s in (job.get("required_skills") or [])[:3]])
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">#{job['id']} {job['title']}</div>
                    <div class="candidate-info">
                        👤 {job.get('posted_by','HR')} &nbsp;·&nbsp; ⏱️ {job.get('min_experience','Any')} yrs exp
                    </div>
                    <div style="margin-top:8px">{skills_html}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-msg">No jobs posted yet. Post a job first.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Upload CV
# ─────────────────────────────────────────────
elif page == "📄 Upload CV":

    st.markdown("""
    <div class="main-header">
        <h1>📄 Upload CV</h1>
        <p>Upload PDF or DOCX files · Data is automatically extracted and saved to the database</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**📁 Select CV File**")

        uploaded = st.file_uploader(
            "Choose a CV file",
            type=["pdf", "docx"],
            help="PDF and DOCX formats are supported"
        )

        if uploaded:
            st.markdown(f"""
            <div class="success-msg">
                ✅ File selected: <strong>{uploaded.name}</strong> ({round(uploaded.size/1024,1)} KB)
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Upload & Process CV", use_container_width=True):
            if not uploaded:
                st.markdown('<div class="error-msg">⚠️ Please select a CV file first!</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Processing CV..."):
                    files = {"file": (uploaded.name, uploaded.getvalue(), "application/octet-stream")}
                    success, res = api_post("/upload-cv", files=files)

                if success:
                    st.markdown(f"""
                    <div class="success-msg">
                        🎉 <strong>Success!</strong> CV uploaded successfully!<br>
                        Candidate ID: <strong>#{res.get('candidate_id')}</strong> &nbsp;·&nbsp;
                        Name: <strong>{res.get('name') or 'Extracted from CV'}</strong>
                    </div>""", unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f'<div class="error-msg">❌ Error: {res.get("detail","Unknown error")}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**📊 Upload Info**")

        ok, data = api_get("/candidates")
        if ok:
            total = data.get("total", 0)
            st.markdown(f"""
            <div style="text-align:center; padding:20px;">
                <div class="metric-number">{total}</div>
                <div class="metric-label">Total CVs in Database</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <hr class="custom-divider">
        <div style="color: #64748b; font-size: 0.88rem; line-height: 1.8;">
            ✅ PDF and DOCX formats supported<br>
            ✅ Name, Email, Phone auto-extracted<br>
            ✅ Skills automatically detected<br>
            ✅ Education & Experience parsed<br>
            ✅ Data saved to PostgreSQL database
        </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Post Job
# ─────────────────────────────────────────────
elif page == "💼 Post Job":

    st.markdown("""
    <div class="main-header">
        <h1>💼 Post a Job</h1>
        <p>Create a new job posting and define the required skills for matching</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**📋 Job Details**")

        job_title = st.text_input("🏷️ Job Title *", placeholder="e.g. Senior Python Developer")
        job_desc  = st.text_area("📝 Job Description", placeholder="Describe the role and responsibilities...", height=120)

        c_exp, c_hr = st.columns(2)
        with c_exp:
            min_exp = st.number_input("⏱️ Min. Experience (years)", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
        with c_hr:
            posted_by = st.text_input("👤 Posted By", value="HR Team")

        st.markdown("**🛠️ Required Skills**")
        skills_input = st.text_area(
            "Enter one skill per line",
            placeholder="Python\nDjango\nREST API\nPostgreSQL\nDocker",
            height=150
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📤 Post Job", use_container_width=True):
            if not job_title:
                st.markdown('<div class="error-msg">⚠️ Please enter a Job Title!</div>', unsafe_allow_html=True)
            elif not skills_input.strip():
                st.markdown('<div class="error-msg">⚠️ Please enter at least one required skill!</div>', unsafe_allow_html=True)
            else:
                skills = [s.strip() for s in skills_input.strip().split('\n') if s.strip()]

                with st.spinner("Posting job..."):
                    success, res = api_post("/post-job", data={
                        "title": job_title,
                        "description": job_desc,
                        "min_experience": min_exp,
                        "required_skills": skills,
                        "posted_by": posted_by
                    })

                if success:
                    st.markdown(f"""
                    <div class="success-msg">
                        🎉 <strong>Job Posted Successfully!</strong><br>
                        Job ID: <strong>#{res.get('job_id')}</strong> &nbsp;·&nbsp;
                        Title: <strong>{res.get('title')}</strong>
                    </div>""", unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f'<div class="error-msg">❌ Error: {res.get("detail","Unknown error")}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**👀 Live Preview**")

        if job_title or skills_input:
            skills_preview = [s.strip() for s in (skills_input or "").strip().split('\n') if s.strip()]
            skills_html = "".join([f'<span class="skill-tag-green">{s}</span>' for s in skills_preview])
            st.markdown(f"""
            <div class="job-card">
                <div class="job-title">{job_title or "Job Title..."}</div>
                <div class="candidate-info">
                    👤 {posted_by or "HR"} &nbsp;·&nbsp; ⏱️ {min_exp} yrs exp required
                </div>
                <hr class="custom-divider">
                <div style="font-size:0.85rem; color:#64748b; margin-bottom:8px;">Required Skills:</div>
                <div>{skills_html or '<span style="color:#374151">No skills added yet...</span>'}</div>
            </div>
            {f'<div style="color:#64748b; font-size:0.85rem; margin-top:12px; padding:12px; background:#0d1525; border-radius:8px; border:1px solid #1e2d4a;">{job_desc[:200]}{"..." if len(job_desc) > 200 else ""}</div>' if job_desc else ""}
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px; color:#374151;">
                <div style="font-size:2.5rem;">💼</div>
                <div style="font-size:0.9rem; margin-top:8px;">Fill in job details to see a live preview here</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Matching
# ─────────────────────────────────────────────
elif page == "🎯 Matching":

    st.markdown("""
    <div class="main-header">
        <h1>🎯 CV – Job Matching</h1>
        <p>Select a job · Calculate match scores · View ranked candidates</p>
    </div>
    """, unsafe_allow_html=True)

    ok, jobs_data = api_get("/jobs")

    if not ok or not jobs_data:
        st.markdown('<div class="error-msg">⚠️ No jobs found! Please post a job first.</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            job_options = {f"#{j['id']} - {j['title']}": j['id'] for j in jobs_data}
            selected_label = st.selectbox("💼 Select a Job", list(job_options.keys()))
            selected_id = job_options[selected_label]

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_match = st.button("🚀 Calculate Matches", use_container_width=True)

        # Job details
        ok_job, job_detail = api_get(f"/jobs/{selected_id}")
        if ok_job:
            skills_html = "".join([f'<span class="skill-tag-green">{s}</span>' for s in job_detail.get("required_skills", [])])
            st.markdown(f"""
            <div class="section-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="job-title">📋 {job_detail['title']}</div>
                        <div class="candidate-info">
                            👤 {job_detail.get('posted_by','HR')} &nbsp;·&nbsp;
                            ⏱️ Min {job_detail.get('min_experience','Any')} years experience
                        </div>
                    </div>
                    <span style="color:#34d399; font-size:0.8rem; background:rgba(52,211,153,0.1);
                                padding:4px 12px; border-radius:20px; border:1px solid rgba(52,211,153,0.3);">
                        {job_detail.get('status','active').upper()}
                    </span>
                </div>
                <hr class="custom-divider">
                <div style="font-size:0.85rem; color:#64748b; margin-bottom:8px;">Required Skills:</div>
                <div>{skills_html}</div>
            </div>""", unsafe_allow_html=True)

        # Run matching
        if run_match:
            with st.spinner("Calculating match scores..."):
                success, match_data = api_post(f"/match/{selected_id}")

            if success:
                matches = match_data.get("matches", [])
                st.markdown(f"""
                <div class="success-msg">
                    ✅ Matching complete! Found <strong>{len(matches)}</strong> candidate(s)
                </div>""", unsafe_allow_html=True)

                if matches:
                    st.markdown("### 🏆 Ranked Candidates")

                    for i, c in enumerate(matches):
                        score  = c.get("match_score", 0)
                        sc     = score_class(score)
                        bc     = bar_class(score)
                        medal  = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"

                        matched_html = "".join([f'<span class="skill-tag-green">✓ {s}</span>' for s in c.get("matched_skills",[])])
                        missing_html = "".join([f'<span class="skill-tag-red">✗ {s}</span>'   for s in c.get("missing_skills",[])])

                        st.markdown(f"""
                        <div class="candidate-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <span style="font-size:1.4rem;">{medal}</span>
                                    <div>
                                        <div class="candidate-name">{c.get('name') or 'Unknown'}</div>
                                        <div class="candidate-info">
                                            📧 {c.get('email') or 'N/A'} &nbsp;·&nbsp;
                                            📞 {c.get('phone') or 'N/A'} &nbsp;·&nbsp;
                                            ⏱️ {c.get('total_exp') or 'N/A'} yrs exp
                                        </div>
                                    </div>
                                </div>
                                <span class="{sc}">{score}%</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="{bc}" style="width:{int(score)}%"></div>
                            </div>
                            <hr class="custom-divider">
                            <div style="display:flex; gap:24px; flex-wrap:wrap;">
                                <div>
                                    <div style="font-size:0.78rem; color:#64748b; margin-bottom:4px;">
                                        ✅ MATCHED ({len(c.get('matched_skills',[]))})
                                    </div>
                                    <div>{matched_html or '<span style="color:#374151">None</span>'}</div>
                                </div>
                                <div>
                                    <div style="font-size:0.78rem; color:#64748b; margin-bottom:4px;">
                                        ❌ MISSING ({len(c.get('missing_skills',[]))})
                                    </div>
                                    <div>{missing_html or '<span style="color:#374151">None</span>'}</div>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-msg">No candidates found in the database.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-msg">❌ {match_data.get("detail","Error occurred")}</div>', unsafe_allow_html=True)

        else:
            # Show saved results
            ok_r, saved = api_get(f"/match/{selected_id}")
            if ok_r and saved.get("matches"):
                st.markdown("### 📊 Previous Match Results")
                for i, c in enumerate(saved["matches"]):
                    score = c.get("match_score", 0)
                    sc = score_class(score)
                    st.markdown(f"""
                    <div class="candidate-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div class="candidate-name">#{i+1} {c.get('name') or 'Unknown'}</div>
                                <div class="candidate-info">📧 {c.get('email') or 'N/A'}</div>
                            </div>
                            <span class="{sc}">{score}%</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:center; padding:50px; color:#374151;">
                    <div style="font-size:2.5rem;">🎯</div>
                    <div style="font-size:0.9rem; margin-top:12px;">
                        Press "Calculate Matches" to find the best candidates for this job
                    </div>
                </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Candidates
# ─────────────────────────────────────────────
elif page == "👥 Candidates":

    st.markdown("""
    <div class="main-header">
        <h1>👥 All Candidates</h1>
        <p>Browse all candidates stored in the database</p>
    </div>
    """, unsafe_allow_html=True)

    ok, data = api_get("/candidates")

    if ok and data.get("candidates"):
        st.markdown(f"**{data['total']} candidates found**")
        search = st.text_input("🔍 Search by name or email", placeholder="Type to filter...")
        st.markdown("<br>", unsafe_allow_html=True)

        for c in data["candidates"]:
            name  = c.get("name") or ""
            email = c.get("email") or ""
            if search and search.lower() not in name.lower() and search.lower() not in email.lower():
                continue

            skills_html = "".join([f'<span class="skill-tag-blue">{s}</span>' for s in (c.get("skills") or [])])

            st.markdown(f"""
            <div class="candidate-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="candidate-name">
                            <span style="color:#374151;">#{c['id']}</span> &nbsp; {name or 'Unknown'}
                        </div>
                        <div class="candidate-info" style="margin-top:6px;">
                            📧 {email or 'N/A'} &nbsp;·&nbsp;
                            📞 {c.get('phone') or 'N/A'} &nbsp;·&nbsp;
                            ⏱️ {c.get('total_exp') or 'N/A'} yrs exp
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#374151;">
                        {str(c.get('created_at',''))[:10]}
                    </div>
                </div>
                <hr class="custom-divider">
                <div style="font-size:0.78rem; color:#64748b; margin-bottom:6px;">
                    Skills ({len(c.get('skills',[]) or [])}):
                </div>
                <div>{skills_html or '<span style="color:#374151">No skills detected</span>'}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:60px; color:#374151;">
            <div style="font-size:3rem;">📭</div>
            <div style="font-size:1.1rem; margin-top:12px;">No Candidates Found</div>
            <div style="font-size:0.85rem; margin-top:8px;">Upload a CV to get started</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: Jobs List
# ─────────────────────────────────────────────
elif page == "📋 Jobs List":

    st.markdown("""
    <div class="main-header">
        <h1>📋 All Jobs</h1>
        <p>Browse all job postings and their required skills</p>
    </div>
    """, unsafe_allow_html=True)

    ok, data = api_get("/jobs")

    if ok and isinstance(data, list) and len(data) > 0:
        st.markdown(f"**{len(data)} jobs found**")
        st.markdown("<br>", unsafe_allow_html=True)

        for job in data[::-1]:
            skills_html = "".join([f'<span class="skill-tag-green">{s}</span>' for s in (job.get("required_skills") or [])])
            status = job.get("status", "active")
            s_color  = "#34d399" if status == "active" else "#64748b"
            s_bg     = "rgba(52,211,153,0.1)" if status == "active" else "rgba(100,116,139,0.1)"
            s_border = "rgba(52,211,153,0.3)" if status == "active" else "rgba(100,116,139,0.3)"

            desc = job.get("description") or ""
            desc_html = f'<div style="margin-top:12px; color:#64748b; font-size:0.85rem; padding:10px; background:#0d1525; border-radius:8px; border:1px solid #1e2d4a;">{desc[:200]}{"..." if len(desc) > 200 else ""}</div>' if desc else ""

            st.markdown(f"""
            <div class="section-card" style="border-left: 3px solid #3b82f6;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="job-title">#{job['id']} &nbsp; {job['title']}</div>
                        <div class="candidate-info" style="margin-top:6px;">
                            👤 {job.get('posted_by','HR')} &nbsp;·&nbsp;
                            ⏱️ Min {job.get('min_experience','Any')} yrs exp &nbsp;·&nbsp;
                            📅 {str(job.get('created_at',''))[:10]}
                        </div>
                    </div>
                    <span style="color:{s_color}; background:{s_bg}; border:1px solid {s_border};
                                padding:4px 12px; border-radius:20px; font-size:0.78rem; font-family:monospace;">
                        {status.upper()}
                    </span>
                </div>
                <hr class="custom-divider">
                <div style="font-size:0.8rem; color:#64748b; margin-bottom:8px;">
                    Required Skills ({len(job.get('required_skills',[]) or [])}):
                </div>
                <div>{skills_html or '<span style="color:#374151">No skills defined</span>'}</div>
                {desc_html}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:60px; color:#374151;">
            <div style="font-size:3rem;">📭</div>
            <div style="font-size:1.1rem; margin-top:12px;">No Jobs Found</div>
            <div style="font-size:0.85rem; margin-top:8px;">Post a job to get started</div>
        </div>""", unsafe_allow_html=True)
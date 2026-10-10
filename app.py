
import streamlit as st
from pypdf import PdfReader
from docx import Document
from io import BytesIO
import re

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Job Matching Portal",
    page_icon="🤖",
    layout="wide"
)

# LIGHT PASTEL COLOURS
st.markdown("""
<style>
.stApp {
    background: #F5F8FF;
    color: #243657;
}
.block-container {
    max-width: 1300px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero {
    background: linear-gradient(110deg, #C7E0FF, #E3D1FF);
    border: 1px solid #D8DFFF;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}
.hero h1 {
    color: #193765;
    margin: 0;
    font-size: 30px;
}
.hero p {
    color: #45618B;
    margin: 6px 0 0;
}
.panel {
    background: #FFFFFF;
    border: 1px solid #DDE7F8;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 3px 12px #7894BD12;
}
.metric {
    background: #FFFFFF;
    border: 1px solid #DCE7FA;
    border-radius: 14px;
    padding: 16px 8px;
    text-align: center;
    min-height: 125px;
}
.metric h2 {
    color: #477BE8;
    margin: 8px 0;
    font-size: 27px;
}
.metric p {
    color: #526887;
    font-size: 13px;
    margin: 0;
}
.metric h3 {
    font-size: 19px;
    margin: 10px 0;
}
.green {
    background: #F0FBF7;
    border: 1px solid #C5EEE0;
}
.pink {
    background: #FFF4F8;
    border: 1px solid #F6D8E7;
}
.blue {
    background: #F0F6FF;
    border: 1px solid #D4E4FF;
}
.orange {
    background: #FFF8EB;
    border: 1px solid #F6E3BD;
}
.purple {
    background: #F6F2FF;
    border: 1px solid #E2D7FF;
}
.tag {
    display: inline-block;
    background: #DFF6ED;
    color: #16775D;
    padding: 7px 13px;
    border-radius: 20px;
    margin: 3px;
    font-size: 12px;
    font-weight: 600;
}
.skill-gap {
    background: #FFFFFF;
    border: 1px solid #F5E8D3;
    border-radius: 9px;
    padding: 9px 12px;
    margin: 5px 0;
    color: #405574;
}
.roadmap-item {
    background: #FFFFFF;
    border: 1px solid #DDEFE9;
    border-radius: 10px;
    padding: 11px;
    margin: 7px 0;
}
.stButton > button {
    background: #6488F5;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
}
.stButton > button:hover {
    background: #496FE0;
    color: #FFFFFF;
}
[data-testid="stFileUploader"] {
    background: #F5F8FF;
    border: 1px dashed #B9CDF5;
    border-radius: 12px;
    padding: 10px;
}
h2, h3, h4 {
    color: #233F70;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="hero">
    <h1>🤖 AI Job Matching Portal</h1>
    <p>AI-powered Resume &amp; Job Compatibility Analysis</p>
</div>
""", unsafe_allow_html=True)

# JOB SKILLS
job_requirements = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Statistics", "Pandas", "NumPy", "Data Analysis"
    ],
    "Business Analyst": [
        "Excel", "SQL", "Power BI", "Communication",
        "Business Analysis", "Requirements", "Documentation",
        "Data Analysis"
    ],
    "Python Developer": [
        "Python", "SQL", "Django", "Flask",
        "API", "OOP", "Git", "Problem Solving"
    ],
    "Software Engineer": [
        "Python", "Java", "SQL", "Git",
        "Data Structures", "Algorithms", "OOP",
        "Problem Solving"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "Python",
        "React", "SQL", "API", "Git"
    ]
}

# LEARNING ROADMAP
roadmap = {
    "Python": "Practice Python basics and build small projects.",
    "SQL": "Learn queries, joins, grouping and filtering.",
    "Excel": "Practice formulas, pivot tables and charts.",
    "Power BI": "Build dashboards and learn data visualization.",
    "Statistics": "Learn averages, probability and basic statistics.",
    "Pandas": "Practice data cleaning using Pandas.",
    "NumPy": "Learn arrays and numerical operations.",
    "Data Analysis": "Practice cleaning and analysing datasets.",
    "Communication": "Practice explaining your work clearly.",
    "Business Analysis": "Learn business processes and requirements.",
    "Requirements": "Practice writing clear project requirements.",
    "Documentation": "Learn to write project documents.",
    "Django": "Build a small Django web application.",
    "Flask": "Create a basic web application using Flask.",
    "API": "Learn how to use and create APIs.",
    "OOP": "Practice classes, objects and inheritance.",
    "Git": "Learn version control and GitHub.",
    "Problem Solving": "Solve beginner programming problems.",
    "Java": "Practice Java and object-oriented programming.",
    "Data Structures": "Learn arrays, stacks, queues and trees.",
    "Algorithms": "Practice searching and sorting algorithms.",
    "HTML": "Build simple web pages using HTML.",
    "CSS": "Practice layouts and responsive design.",
    "JavaScript": "Learn variables, functions and DOM basics.",
    "React": "Build small components and a simple app."
}

# RESUME UPLOAD AND JOB SELECTION
left, right = st.columns([0.9, 2.1], gap="medium")

resume_text = ""
uploaded_file = None

with left:
    st.markdown(
        '<div class="panel"><h3>📄 Resume &amp; Job Details</h3>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:
        try:
            filename = uploaded_file.name.lower()

            if filename.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                resume_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

            elif filename.endswith(".docx"):
                document = Document(
                    BytesIO(uploaded_file.getvalue())
                )
                resume_text = "\n".join(
                    p.text for p in document.paragraphs
                )

            elif filename.endswith(".txt"):
                resume_text = uploaded_file.getvalue().decode(
                    "utf-8", errors="ignore"
                )

            st.success("Resume uploaded successfully!")
            st.caption(uploaded_file.name)

        except Exception as error:
            st.error(f"Could not read resume: {error}")

    job_role = st.selectbox(
        "Select your interested job role",
        list(job_requirements.keys())
    )

    st.markdown('</div>', unsafe_allow_html=True)

# MATCHING LOGIC
required = job_requirements[job_role]

if resume_text.strip():
    resume_lower = resume_text.lower()

    matched = [
        skill for skill in required
        if re.search(
            r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)",
            resume_lower
        )
    ]

    missing = [
        skill for skill in required
        if skill not in matched
    ]

    match_percent = round(
        len(matched) / len(required) * 100
    )

    all_skills = sorted(
        {skill for skills in job_requirements.values()
         for skill in skills},
        key=len,
        reverse=True
    )

    detected_skills = [
        skill for skill in all_skills
        if re.search(
            r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)",
            resume_lower
        )
    ]
else:
    matched = []
    missing = required
    match_percent = 0
    detected_skills = []

# JOB MATCH DASHBOARD
with right:
    st.markdown("### 📊 Job Match Dashboard")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric blue">
            <p>Overall Match</p>
            <h2>{match_percent}%</h2>
            <p>Required skills</p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric green">
            <p>Job Skill Match</p>
            <h2>{match_percent}%</h2>
            <p>Skills matched</p>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric purple">
            <p>AI Semantic Match</p>
            <h2>{match_percent}%</h2>
            <p>Keyword-based demo</p>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        if match_percent >= 75:
            level = "Strong Match"
        elif match_percent >= 40:
            level = "Moderate Match"
        else:
            level = "Low Match"

        st.markdown(f"""
        <div class="metric orange">
            <p>⭐ Match Level</p>
            <h3>{level}</h3>
            <p>Based on skills</p>
        </div>
        """, unsafe_allow_html=True)

    # QUICK ANALYSIS - THREE DIFFERENT COLOURS
    st.markdown("### ⚡ Quick Analysis")

    q1, q2, q3 = st.columns(3)

    with q1:
        st.markdown(f"""
        <div style="
            background:#E4F8EF;
            border:1px solid #BDEBD7;
            border-radius:12px;
            padding:16px;
            color:#176B50;
            text-align:center;
            min-height:100px;
        ">
            <div>✅ Matched Skills</div>
            <h2 style="color:#168664;margin:8px 0;">
                {len(matched)}
            </h2>
            <small>Skills matched</small>
        </div>
        """, unsafe_allow_html=True)

    with q2:
        st.markdown(f"""
        <div style="
            background:#FFF0F5;
            border:1px solid #F5CFDF;
            border-radius:12px;
            padding:16px;
            color:#9D426A;
            text-align:center;
            min-height:100px;
        ">
            <div>🚀 Skills to Learn</div>
            <h2 style="color:#D65387;margin:8px 0;">
                {len(missing)}
            </h2>
            <small>Recommended skills</small>
        </div>
        """, unsafe_allow_html=True)

    with q3:
        st.markdown(f"""
        <div style="
            background:#EAF3FF;
            border:1px solid #C8DCFF;
            border-radius:12px;
            padding:16px;
            color:#315A9B;
            text-align:center;
            min-height:100px;
        ">
            <div>🎯 Job Required Skills</div>
            <h2 style="color:#477BE8;margin:8px 0;">
                {len(required)}
            </h2>
            <small>Required skills</small>
        </div>
        """, unsafe_allow_html=True)

# MATCHING SKILLS AND REQUIRED SKILLS
st.divider()

a, b = st.columns(2, gap="medium")

with a:
    st.markdown(
        '<div class="panel green"><h3>✅ Your Matching Skills</h3>',
        unsafe_allow_html=True
    )

    if matched:
        tags = " ".join(
            f'<span class="tag">{skill}</span>'
            for skill in matched
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.write("Upload a readable resume to detect matching skills.")

    st.markdown('</div>', unsafe_allow_html=True)

with b:
    st.markdown(
        '<div class="panel pink"><h3>🚀 Skills Required for This Job</h3>',
        unsafe_allow_html=True
    )

    if missing:
        tags = " ".join(
            f'<span class="tag">{skill}</span>'
            for skill in missing
        )
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.success("All listed skills matched!")

    with st.expander("👁️ View Detailed Skill Detection"):
        st.write("**Selected job:**", job_role)
        st.write("**Required skills:**", ", ".join(required))
        st.write("**Matched skills:**", ", ".join(matched) or "None")
        st.write("**Skills to learn:**", ", ".join(missing) or "None")

    st.markdown('</div>', unsafe_allow_html=True)

# AI MATCHING INSIGHTS
st.markdown(
    '<div class="panel blue"><h3>🧠 AI Matching Insights</h3>',
    unsafe_allow_html=True
)

i1, i2 = st.columns(2)

with i1:
    st.markdown("#### 🎯 Skill-Based Analysis")
    st.write(
        f"Your resume matches {len(matched)} out of "
        f"{len(required)} listed job skills."
    )
    st.progress(match_percent / 100)
    st.write(f"**Skill Match: {match_percent}%**")

with i2:
    st.markdown("#### 🧠 Semantic Analysis")
    st.write(
        "This demo compares keywords in your resume "
        "with the selected job's required skills."
    )
    st.write("A real semantic AI model can be added later.")
    st.write(f"**Keyword Match: {match_percent}%**")

st.markdown('</div>', unsafe_allow_html=True)

# SKILL GAP ANALYSIS AND CAREER ROADMAP
c, d = st.columns(2, gap="medium")

with c:
    st.markdown(
        '<div class="panel orange"><h3>🎯 AI Skill Gap Analysis</h3>',
        unsafe_allow_html=True
    )

    if missing:
        for skill in missing:
            st.markdown(
                f'<div class="skill-gap">📘 <b>{skill}</b>'
                ' — Recommended Learning</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("Great! No missing skills from this list.")

    st.markdown('</div>', unsafe_allow_html=True)

with d:
    st.markdown(
        '<div class="panel green"><h3>🛣️ Career Preparation Roadmap</h3>',
        unsafe_allow_html=True
    )

    if missing:
        for index, skill in enumerate(missing[:4], start=1):
            description = roadmap.get(
                skill,
                "Learn the basics and practise with a small project."
            )
            st.markdown(f"""
            <div class="roadmap-item">
                <b>🔹 {index}. Learn {skill}</b><br>
                <span style="color:#526887;font-size:13px;">
                    {description}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Keep practising and build projects for your portfolio.")

    st.markdown('</div>', unsafe_allow_html=True)

# RESUME SUMMARY
st.markdown(
    '<div class="panel purple"><h3>📑 Resume Analysis Summary</h3>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

s1.metric("Resume Skills Detected", len(detected_skills))
s2.metric("Job Skills", len(required))
s3.metric("Matched Skills", len(matched))

st.caption(
    "Note: This project demo uses keyword matching. "
    "Results depend on readable resume text and the selected job role."
)

st.markdown('</div>', unsafe_allow_html=True)
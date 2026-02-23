import streamlit as st
import os
import json
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

# ---------------- SESSION STATE ----------------
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "parsed_resumes" not in st.session_state:
    st.session_state.parsed_resumes = None

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

st.title("AI Candidate Screening Tool")

jd = st.text_area("Paste Job Description Here")
resumes = st.text_area("Paste Resumes (Separate each resume with ###)")

# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze"):

    if not jd or not resumes:
        st.warning("Please provide both JD and resumes.")
    else:
        # ✅ FIXED resume splitting
        resume_list = [r.strip() for r in resumes.split("###") if r.strip()]

        with st.spinner("Analyzing Job Description..."):

            jd_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a strict parser.

Extract required skills and minimum experience from the job description.

Rules:
- Return ONLY valid JSON.
- Do NOT explain anything.
- Do NOT add extra text.

Format:
{
  "required_skills": [],
  "minimum_experience_years": number
}
"""
                    },
                    {"role": "user", "content": jd}
                ]
            )

        raw_jd = jd_response.choices[0].message.content.strip()

        start = raw_jd.find("{")
        end = raw_jd.rfind("}") + 1
        clean_jd = raw_jd[start:end]

        try:
            jd_data = json.loads(clean_jd)
        except:
            st.error("Failed to parse JD JSON.")
            jd_data = {"required_skills": [], "minimum_experience_years": 0}

        required_skills = [s.lower() for s in jd_data.get("required_skills", [])]
        minimum_exp = jd_data.get("minimum_experience_years", 0)

        # Store in session
        st.session_state.analysis_data = {
            "required_skills": required_skills,
            "minimum_exp": minimum_exp,
        }

        # ---------------- PARSE RESUMES ONCE ----------------
        parsed_resumes = []

        for resume in resume_list:

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a strict resume parser.

Your task:
Extract structured data from ONE resume only.

Rules:
- Return ONLY valid JSON.
- Do NOT explain anything.
- Do NOT add extra text.
- Do NOT combine multiple resumes.
- If multiple education entries exist, return the highest degree only.
- If multiple numbers appear, select total professional experience only.

Format:
{
  "skills": [],
  "experience_years": number,
  "education": ""
}
"""
                    },
                    {"role": "user", "content": resume}
                ]
            )

            raw_output = response.choices[0].message.content.strip()

            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1

            if start == -1 or end == -1:
                parsed_resumes.append(None)
                continue

            clean_json = raw_output[start:end]

            try:
                resume_data = json.loads(clean_json)
                parsed_resumes.append(resume_data)
            except:
                parsed_resumes.append(None)

        st.session_state.parsed_resumes = parsed_resumes

# ---------------- IF ANALYSIS EXISTS ----------------
if st.session_state.analysis_data and st.session_state.parsed_resumes:

    required_skills = st.session_state.analysis_data["required_skills"]
    minimum_exp = st.session_state.analysis_data["minimum_exp"]
    parsed_resumes = st.session_state.parsed_resumes

    st.subheader("Adjust Scoring Weights")

    skill_weight = st.slider("Skill Importance", 1, 5, 3)
    experience_weight = st.slider("Experience Importance", 1, 5, 2)

    st.divider()
    st.subheader("Candidate Analysis")

    all_results = []

    for i, resume_data in enumerate(parsed_resumes):

        st.markdown(f"### Resume {i+1}")

        if not resume_data:
            st.error("Failed to parse resume.")
            all_results.append((f"Resume {i+1}", 0))
            continue

        st.code(json.dumps(resume_data, indent=2), language="json")

        candidate_skills = [s.lower() for s in resume_data.get("skills", [])]
        candidate_exp = resume_data.get("experience_years", 0)

        # Skill Matching
        matched_skills = []
        for req in required_skills:
            for cand in candidate_skills:
                if req in cand or cand in req:
                    matched_skills.append(req)

        skill_score = len(set(matched_skills))

        # Experience Matching
        experience_match = candidate_exp >= minimum_exp
        experience_score = 1 if experience_match else 0

        # Weighted Score
        total_score = (skill_score * skill_weight) + (experience_score * experience_weight)

        st.write("Matched Skills:", list(set(matched_skills)))
        st.write("Experience Match:", experience_match)
        st.success(f"Final Weighted Score: {total_score}")

        explanation = f"""
Matched {skill_score} required skills.
Experience requirement met: {experience_match}.
Score formula:
({skill_score} × {skill_weight}) + ({experience_score} × {experience_weight})
= {total_score}
"""
        st.info(explanation)

        all_results.append((f"Resume {i+1}", total_score))

    st.divider()

    # -------- Final Ranking --------
    st.subheader("Final Candidate Ranking")

    sorted_results = sorted(all_results, key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(sorted_results, columns=["Candidate", "Score"])

    st.dataframe(df, use_container_width=True)

    if len(sorted_results) > 0:
        top_candidate = sorted_results[0]
        st.success(f"🏆 Top Candidate: {top_candidate[0]} with Score {top_candidate[1]}")

        avg_score = sum([s for _, s in sorted_results]) / len(sorted_results)
        st.write(f"📊 Average Candidate Score: {round(avg_score, 2)}")

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Ranking as CSV",
        data=csv,
        file_name="candidate_ranking.csv",
        mime="text/csv",
    )
# 🚀 AI Candidate Screening Tool

An AI-powered resume screening application that extracts job requirements, evaluates candidates against them, and generates a transparent, ranked shortlist using adjustable scoring weights.

---

## 🧠 Overview

Recruiters often spend hours manually screening resumes for a single role. This tool automates first-level screening by:

- Extracting required skills and experience from a Job Description
- Parsing resumes into structured data using AI
- Matching candidates against job requirements
- Applying weighted scoring logic
- Generating ranked shortlists with explanations
- Allowing CSV export of results

The goal is to reduce manual screening time while maintaining transparency and recruiter control.

---

## 🌐 Live Demo

👉 **Access the live application here:**  
https://YOUR-STREAMLIT-LINK.streamlit.app  

✅ No login required  
✅ No installation required  
✅ Fully browser-based  

---

## ⚡ How It Works

1. **Paste Job Description**  
   Add the job requirements in the first input box.

2. **Paste Resumes**  
   Add one or more resumes in the second box.  
   Separate each resume using:

3. **Click Analyze**  
The system:
- Extracts required skills & minimum experience
- Parses resumes into structured data
- Matches candidates against requirements

4. **Adjust Scoring Weights (Optional)**  
Use sliders to control:
- Skill Importance
- Experience Importance

5. **View Ranked Results**  
Candidates are ranked automatically based on a weighted score.

6. **Download CSV (Optional)**  
Export the ranked shortlist instantly.

---

## 🎯 Features

- 🤖 AI-powered job requirement extraction
- 📄 Resume parsing into structured JSON
- 🎯 Skill matching engine
- ⚖️ Adjustable weighted scoring
- 📊 Transparent score breakdown
- 🏆 Automatic candidate ranking
- 📥 CSV export
- ⚡ Real-time re-ranking when sliders change

---

## 🧪 Sample Test Data

### 📌 Sample Job Description

We are hiring a Backend Python Developer.

Requirements:
- Strong knowledge of Python
- Experience with Django or FastAPI
- Experience with AWS services (EC2, S3, Lambda)
- Maintain CI/CD pipelines
- Minimum 3 years of professional experience
- Bachelor’s degree in Computer Science or related field

---

### 📌 Sample Resumes (Copy All Below & seperate them with ###)

5 years of experience in Python and Django.
Strong AWS experience including EC2, Lambda, and S3.
Built distributed systems and scalable APIs.
Maintained CI/CD pipelines.
M.Tech in Software Engineering.
###
2 years experience in Java.
Worked with Spring Boot, MySQL and REST APIs.
Basic exposure to AWS S3.
BCA Graduate.
###
6 years experience in Python, FastAPI, AWS (EC2, Lambda, S3).
Strong backend architecture design.
Experience managing CI/CD pipelines.
Bachelor’s degree in Computer Science.
###
3 years experience in Python and Flask.
Worked on AWS EC2 deployments.
Bachelor’s degree in Computer Applications.
###
8 years experience in Node.js and Express.
Worked with Azure cloud services.
MBA in IT Management.
###
3 years experience in Python, FastAPI, AWS EC2 and Lambda.
Bachelor’s degree in Computer Science.
###
5 years experience in Python.
Worked on Data Analysis and Machine Learning.
Experience with AWS S3.
B.Tech in Information Technology.

---

## 🤖 AI & Scoring Architecture

### AI Model
- Llama 3.1 via Groq API
- Used strictly for structured data extraction

### Deterministic Scoring Logic

The scoring engine is implemented in Python to ensure transparency.

Final Score = (Skill Matches × Skill Weight) + (Experience Match × Experience Weight)

Where:
- Skill Matches = Number of required skills matched
- Experience Match = 1 if candidate meets minimum experience, else 0
- Skill Weight & Experience Weight are adjustable by the recruiter

---

## 🛠 Tech Stack

- Python
- Streamlit
- Groq API (Llama 3.1)
- JSON parsing
- Custom matching & ranking engine

---

## 📦 Repository Structure

- app.py
- requirements.txt
- README.md


---

## 🔐 Security & Data Handling

- No user data is stored
- API keys are managed via environment variables
- No authentication required
- Fully client-accessible via browser

---

## 🎯 Problem This Solves

Recruiters reviewing 100–200 resumes per role spend significant time on manual screening.

This tool:

- Reduces screening time
- Standardises evaluation
- Improves transparency
- Enables recruiter-controlled prioritisation
- Produces ranked shortlists instantly

---

## 🚀 Built For

Associate Product Manager Screening Assignment

This MVP demonstrates:

- Product thinking
- AI integration
- Scoring design
- Recruiter-centric workflow
- Explainable ranking logic
- Clean MVP execution


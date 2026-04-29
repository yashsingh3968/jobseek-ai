import streamlit as st
import requests

API_BASE = "http://localhost:5000"

st.title("JobSeek AI")
st.subheader("AI-powered Job Search Platform 🚀")

# -------------------------
# JOB SEARCH
# -------------------------
st.header("🔍 Search Jobs")

query = st.text_input("Enter job keyword (e.g. python)")
location = st.text_input("Location")

if st.button("Search Jobs"):
    params = {"q": query, "location": location}

    try:
        res = requests.get(f"{API_BASE}/api/jobs", params=params)
        jobs = res.json()

        if jobs:
            for job in jobs:
                st.write("###", job["title"])
                st.write("Company:", job["company"])
                st.write("Location:", job["location"])
                st.write("Ghost Score:", job["ghost_score"])
                st.write("---")
        else:
            st.warning("No jobs found")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# RESUME UPLOAD
# -------------------------
st.header("📄 Upload Resume")

email = st.text_input("Enter your email")
resume_text = st.text_area("Paste your resume text")

if st.button("Analyze Resume"):
    data = {
        "email": email,
        "resume_text": resume_text
    }

    try:
        res = requests.post(f"{API_BASE}/api/users/resume", json=data)
        result = res.json()

        st.success("Resume processed!")

        st.write("### Extracted Skills:")
        st.write(result.get("skills", []))

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# MATCHING
# -------------------------
st.header("🎯 Get Job Matches")

match_email = st.text_input("Enter email for matching")

if st.button("Find Matches"):
    try:
        res = requests.get(f"{API_BASE}/api/matches", params={"email": match_email})
        matches = res.json()

        if isinstance(matches, list):
            for m in matches:
                st.write("###", m["title"])
                st.write("Company:", m["company"])
                st.write("Match Score:", m["match_score"])
                st.write("---")
        else:
            st.error(matches)

    except Exception as e:
        st.error(f"Error: {e}")
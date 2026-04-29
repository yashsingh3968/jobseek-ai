import streamlit as st
import requests
import pandas as pd

# Define the base URL of your Flask API
API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Job Hunter Portal", layout="wide")

st.title("🎯 Job Hunter Portal")
st.write("Find jobs, upload your resume, and get personalized matches.")

# Create tabs for the different API features
tab_search, tab_resume, tab_matches = st.tabs([
    "🔍 Job Search", 
    "📄 Upload Resume", 
    "✨ AI Job Matches"
])

# ---------------------------------------------------------
# TAB 1: Job Search (/api/jobs)
# ---------------------------------------------------------
with tab_search:
    st.header("Search for Jobs")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("Job Title / Keywords", placeholder="e.g. Python Developer")
    with col2:
        location = st.text_input("Location", placeholder="e.g. Remote, New York")
    with col3:
        max_ghost = st.slider("Max Ghost Score", min_value=0.0, max_value=1.0, value=0.6, step=0.1, 
                              help="Filter out jobs likely to 'ghost' you.")
        
    if st.button("Search Jobs", type="primary"):
        with st.spinner("Searching..."):
            try:
                params = {
                    "q": search_query,
                    "location": location,
                    "max_ghost": max_ghost
                }
                response = requests.get(f"{API_BASE_URL}/api/jobs", params=params)
                
                if response.status_code == 200:
                    jobs = response.json()
                    if jobs:
                        st.success(f"Found {len(jobs)} jobs!")
                        # Display as a neat dataframe
                        df = pd.DataFrame(jobs)
                        # Reorder columns for better readability
                        df = df[["title", "company", "location", "ghost_score", "source"]]
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No jobs found matching your criteria.")
                else:
                    st.error(f"Error fetching jobs: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is the Flask app running?")

# ---------------------------------------------------------
# TAB 2: Resume Upload (/api/users/resume)
# ---------------------------------------------------------
with tab_resume:
    st.header("Upload Resume & Extract Skills")
    
    email_upload = st.text_input("Email Address", key="email_upload")
    resume_text = st.text_area("Paste your resume text here", height=200)
    
    if st.button("Analyze Resume", type="primary"):
        if not email_upload or not resume_text:
            st.warning("Please provide both an email and resume text.")
        else:
            with st.spinner("Extracting skills via AI..."):
                try:
                    payload = {
                        "email": email_upload,
                        "resume_text": resume_text
                    }
                    response = requests.post(f"{API_BASE_URL}/api/users/resume", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Resume processed successfully!")
                        st.write("**Extracted Skills:**")
                        
                        # Display skills as tags
                        skills = data.get("skills", [])
                        if skills:
                            st.write(", ".join([f"`{skill}`" for skill in skills]))
                        else:
                            st.info("No specific skills could be extracted.")
                    else:
                        st.error(f"Error processing resume: {response.json().get('error', 'Unknown Error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend. Is the Flask app running?")

# ---------------------------------------------------------
# TAB 3: Job Matches (/api/matches)
# ---------------------------------------------------------
with tab_matches:
    st.header("Get Personalized Job Matches")
    st.write("Enter your email to find jobs that match your extracted resume skills.")
    
    email_match = st.text_input("Email Address", key="email_match")
    
    if st.button("Find Matches", type="primary"):
        if not email_match:
            st.warning("Please enter your email address.")
        else:
            with st.spinner("Finding the best jobs for you..."):
                try:
                    params = {"email": email_match}
                    response = requests.get(f"{API_BASE_URL}/api/matches", params=params)
                    
                    if response.status_code == 200:
                        matches = response.json()
                        if matches:
                            st.success(f"Top {len(matches)} matches found!")
                            df_matches = pd.DataFrame(matches)
                            # Highlight the match score
                            st.dataframe(
                                df_matches.style.background_gradient(subset=['match_score'], cmap='Greens'),
                                use_container_width=True
                            )
                        else:
                            st.info("No matches found. Try uploading a more detailed resume.")
                    elif response.status_code == 404:
                        st.error("User or skills not found. Have you uploaded your resume in the 'Upload Resume' tab yet?")
                    else:
                        st.error(f"Error fetching matches: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend. Is the Flask app running?")
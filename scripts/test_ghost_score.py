from app.ai_service import ghost_score

job_legit = {
    "title": "Software Engineer – Backend (Python)",
    "company": "Legit Corp",
    "description": "Full-time role with clear responsibilities and 10-20 LPA salary.",
    "location": "Pune",
    "age_days": 3
}

job_sus = {
    "title": "Urgent Opening Fresher",
    "company": "Unknown Pvt Ltd",
    "description": "Salary negotiable. Apply fast. Limited openings. No details.",
    "location": "Remote",
    "age_days": 60
}

print("Legit job score:", ghost_score(job_legit))
print("Suspicious job score:", ghost_score(job_sus))
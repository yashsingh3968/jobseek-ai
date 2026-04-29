from flask import Flask, jsonify, request
from app.db import SessionLocal
from app.models import Job, User
from app.ai_service import extract_skills_from_resume



app = Flask(__name__)

@app.get("/")
def welcome():
    return "Hey, I am up and running!", 200

@app.get("/health")
def health():
    return "OK", 200


@app.get("/api/jobs")
def search_jobs():
    q = request.args.get("q", "").lower()
    location = request.args.get("location", "").lower()
    max_ghost = float(request.args.get("max_ghost", 0.6))

    db = SessionLocal()
    query = db.query(Job)

    if q:
        query = query.filter(Job.title.ilike(f"%{q}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    query = query.filter(
        (Job.ghost_score == None) | (Job.ghost_score <= max_ghost)  # noqa
    )

    jobs = query.order_by(Job.post_date.desc()).limit(50).all()
    db.close()

    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "ghost_score": j.ghost_score,
            "source": j.source,
        }
        for j in jobs
    ])

@app.get("/api/matches")
def match_jobs():
    email = request.args.get("email")

    if not email:
        return {"error": "email required"}, 400

    db = SessionLocal()

    user = db.query(User).filter_by(email=email).first()

    if not user or not user.skills_json:
        db.close()
        return {"error": "user or skills not found"}, 404

    skills = set(user.skills_json)

    jobs = db.query(Job).all()

    results = []

    for j in jobs:
        text = (j.description or "").lower()

        score = sum(1 for s in skills if s in text)

        results.append({
            "title": j.title,
            "company": j.company,
            "match_score": score
        })

    db.close()

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results[:10]


@app.post("/api/users/resume")
def upload_resume():
    data = request.get_json() or {}

    email = data.get("email")
    resume_text = data.get("resume_text", "")

    if not email or not resume_text:
        return {"error": "email and resume_text required"}, 400

    db = SessionLocal()

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(email=email)
        db.add(user)

    user.resume_text = resume_text

    skills = extract_skills_from_resume(resume_text)
    user.skills_json = skills

    db.commit()
    db.refresh(user)
    db.close()

    return {
        "user_id": user.id,
        "skills": skills
    }
if __name__ == "__main__":   # <-- always last
    app.run(debug=True)
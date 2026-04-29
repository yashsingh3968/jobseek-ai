import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
assert api_key, "GEMINI_API_KEY missing"

client = genai.Client(api_key=api_key)

GHOST_PROMPT_TEMPLATE = """
You are an assistant that analyzes job postings for software engineers.

Task:
- Read the job description and metadata.
- Return how likely this job is to be a ghost or fake posting.

Output:
- Return JSON ONLY in this format:
  {{"score": <number between 0 and 1>, "reason": "short explanation"}}

Rules:
- score close to 0.0 = very legitimate
- score close to 1.0 = very likely ghost/fake
- Do not add markdown, code fences, or extra text.

Job data:
Title: {title}
Company: {company}
Description: {description}
Location: {location}
AgeDays: {age_days}
"""


def ghost_score(job: dict) -> tuple[float, str]:
    prompt = GHOST_PROMPT_TEMPLATE.format(
        title=job.get("title", ""),
        company=job.get("company", ""),
        description=job.get("description", ""),
        location=job.get("location", ""),
        age_days=job.get("age_days", ""),
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = (response.text or "").strip()
        data = json.loads(text)

        score = float(data.get("score", 0.5))
        reason = str(data.get("reason", "no reason provided"))
        return score, reason

    except Exception as e:
        print("[ghost_score] Error:", e)
        return 0.5, "error or unknown"
    
SKILL_PROMPT_TEMPLATE = """
You are an assistant that extracts technical skills from a software engineer's resume.

Task:
- Read the resume text.
- Return a JSON array of unique technical skills.

Rules:
- Use lowercase
- Only technical skills (no soft skills)
- Output JSON only

Resume:
{resume_text}
"""


def extract_skills_from_resume(resume_text: str) -> list[str]:
    prompt = SKILL_PROMPT_TEMPLATE.format(resume_text=resume_text)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = (response.text or "").strip()
        skills = json.loads(text)

        if isinstance(skills, list):
            return [str(s).lower() for s in skills]

        return []

    except Exception as e:
        print("[extract_skills] Error:", e)
        return []
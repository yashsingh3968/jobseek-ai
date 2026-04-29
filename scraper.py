import feedparser
from datetime import datetime
import re


def fetch_rss(url: str) -> list[dict]:
    try:
        feed = feedparser.parse(url)
        entries = []

        for e in feed.entries:
            entries.append({
                "title": getattr(e, "title", ""),
                "link": getattr(e, "link", ""),
                "summary": getattr(e, "summary", ""),
                "published": getattr(e, "published", ""),
            })

        return entries

    except Exception as e:
        print("[fetch_rss] Error:", e)
        return []


def normalize_entry(entry: dict, source_name: str) -> dict:
    title = entry.get("title", "").strip()
    summary = entry.get("summary", "")

    description = summary
    company = "Unknown"
    location = "Unknown"
    salary_min = None

    # basic salary detection
    m = re.search(r"(\d+)\s*L", summary)
    if m:
        salary_min = int(m.group(1)) * 100000

    published_str = entry.get("published", "")
    try:
        post_date = datetime.strptime(published_str[:16], "%a, %d %b %Y")
    except Exception:
        post_date = datetime.utcnow()

    return {
        "title": title,
        "company": company,
        "description": description,
        "location": location,
        "salary_min": salary_min,
        "post_date": post_date,
        "source": source_name,
    }

from fuzzywuzzy import fuzz


def dedupe_jobs(jobs: list[dict], threshold: int = 90) -> list[dict]:
    unique = []

    for job in jobs:
        title = job.get("title", "")

        if not any(fuzz.ratio(title, u.get("title", "")) >= threshold for u in unique):
            unique.append(job)

    return unique

from app.ai_service import ghost_score
from app.db import SessionLocal
from app.models import Job
import yaml
from pathlib import Path


def run_scraper():
    config_path = Path("config/sources.yaml")
    data = yaml.safe_load(config_path.read_text())
    sources = data.get("sources", [])

    db = SessionLocal()

    for src in sources:
        url = src["url"]
        name = src["name"]

        raw_entries = fetch_rss(url)
        jobs_raw = [normalize_entry(e, name) for e in raw_entries]
        jobs_unique = dedupe_jobs(jobs_raw)

        for j in jobs_unique:
            score, reason = ghost_score(j)

            job_obj = Job(
                title=j["title"],
                company=j["company"],
                description=j["description"],
                location=j["location"],
                salary_min=j["salary_min"],
                post_date=j["post_date"],
                source=j["source"],
                ghost_score=score,
                ghost_reason=reason,
            )

            db.add(job_obj)

    db.commit()
    db.close()

    print("Scraping complete.")
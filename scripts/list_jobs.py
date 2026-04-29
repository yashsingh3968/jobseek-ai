from app.db import SessionLocal
from app.models import Job

db = SessionLocal()

jobs = db.query(Job).all()

for j in jobs:
    print(j.title, "|", j.ghost_score)

db.close()
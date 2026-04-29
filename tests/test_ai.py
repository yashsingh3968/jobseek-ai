from app.ai_service import ghost_score


def test_ghost_score_basic():
    job = {
        "title": "Python Developer",
        "company": "TestCorp",
        "description": "Looking for Python developer with Django",
        "location": "Pune",
        "age_days": 2
    }

    score, reason = ghost_score(job)

    # Basic validation (don’t depend on API result)
    assert isinstance(score, float)
    assert isinstance(reason, str)
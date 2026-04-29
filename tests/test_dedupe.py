from scraper import dedupe_jobs


def test_dedupe():
    jobs = [
        {"title": "Python Developer"},
        {"title": "Python developer"},
        {"title": "Java Engineer"},
    ]

    unique = dedupe_jobs(jobs)

    assert len(unique) == 2
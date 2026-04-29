import pytest
from api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_jobs_endpoint(client):
    resp = client.get("/api/jobs")
    assert resp.status_code == 200
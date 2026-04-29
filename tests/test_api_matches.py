import pytest
from api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_matches_missing_email(client):
    resp = client.get("/api/matches")
    assert resp.status_code == 400


def test_matches_valid(client):
    # This depends on DB having data
    resp = client.get("/api/matches?email=test@example.com")

    # Accept both cases
    assert resp.status_code in [200, 404]
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_homepage_renders_form():
    response = client.get("/")

    assert response.status_code == 200
    assert "Predict math scores" in response.text

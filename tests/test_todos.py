from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_create_todo():
    response = client.post("/todos/", params={"title": "Buy milk"})
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"

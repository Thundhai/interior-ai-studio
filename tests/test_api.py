import os
import pytest
from fastapi.testclient import TestClient
from src.api import app

API_KEY = os.getenv("INTERIOR_AI_API_KEY", "demo-changeme-not-secure")
client = TestClient(app)

def test_visualization_agent():
    response = client.post(
        "/agent/visualization",
        headers={"x-api-key": API_KEY},
        json={
            "project_id": "test_project",
            "task": {"prompt": "Test moodboard", "type": "moodboard"}
        }
    )
    assert response.status_code == 200
    assert "result" in response.json()
    assert "context" in response.json()

def test_auth_required():
    response = client.post(
        "/agent/visualization",
        json={"project_id": "test_project", "task": {"prompt": "Test", "type": "moodboard"}}
    )
    assert response.status_code == 401

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)
API_KEY = "changeme"  # Set to your test key or use os.environ

def test_budget_endpoint():
    response = client.post("/budget", json={"budget": 1000}, headers={"x-api-key": API_KEY})
    assert response.status_code == 200
    assert "result" in response.json()

def test_material_endpoint():
    response = client.post("/material", json={"material": "flooring"}, headers={"x-api-key": API_KEY})
    assert response.status_code == 200
    assert "result" in response.json()

def test_client_preference_endpoint():
    response = client.post("/client_preference", json={"survey": {"style_tags": ["modern"]}}, headers={"x-api-key": API_KEY})
    assert response.status_code == 200
    assert "result" in response.json()

def test_competitor_insights_endpoint():
    response = client.post("/competitor_insights", json={}, headers={"x-api-key": API_KEY})
    assert response.status_code == 200
    assert "result" in response.json()

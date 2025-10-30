
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from agents.sustainability_advisor_agent import SustainabilityAdvisorAgent
from agents.furniture_advisor_agent import FurnitureAdvisorAgent
from agents.moodboard_agent import MoodBoardAgent

def test_sustainability_advisor_agent_run(monkeypatch):
    agent = SustainabilityAdvisorAgent()
    monkeypatch.setattr(agent, "scrape_archdaily", lambda: [{"title": "Eco", "url": "http://a.com"}])
    monkeypatch.setattr(agent, "scrape_ecowatch", lambda: [{"title": "Green", "url": "http://b.com"}])
    result = agent.run({})
    assert "archdaily" in result and "ecowatch" in result

def test_furniture_advisor_agent_run(monkeypatch):
    agent = FurnitureAdvisorAgent()
    monkeypatch.setattr(agent, "scrape_wayfair", lambda: [{"name": "Chair", "url": "http://w.com", "price": "$100"}])
    monkeypatch.setattr(agent, "scrape_ikea", lambda: [{"name": "Table", "url": "http://i.com", "price": "$200"}])
    result = agent.run({})
    assert "wayfair" in result and "ikea" in result

def test_moodboard_agent_run(monkeypatch):
    agent = MoodBoardAgent(api_token="fake")
    monkeypatch.setattr(agent, "scrape_pinterest", lambda q: ["img1", "img2"])
    monkeypatch.setattr(agent, "scrape_instagram", lambda q: ["img3"])
    monkeypatch.setattr(agent, "generate_collage", lambda imgs: "http://collage.com")
    result = agent.run({"query": "modern"})
    assert "images" in result and "collage_url" in result

import pytest
from agents.visualization_agent import VisualizationAgent
from agents.content_creator_agent import ContentCreatorAgent
from agents.style_advisor_agent import StyleAdvisorAgent

def test_visualization_agent_run():
    agent = VisualizationAgent(api_token="fake-token")
    result = agent.run({"prompt": "Test moodboard"})
    assert "image_url" in result
    assert "materials" in result

def test_content_creator_agent_run():
    agent = ContentCreatorAgent()
    result = agent.run({"type": "blog", "topic": "modern luxury"})
    assert "content" in result


def test_style_advisor_agent_run():
    agent = StyleAdvisorAgent()
    result = agent.run({"topic": "color psychology"})
    assert "trends" in result
    assert "color_psychology" in result
    assert isinstance(result["trends"], list)
    assert isinstance(result["color_psychology"], list)

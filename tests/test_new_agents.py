import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pytest
from agents.budget_cost_advisor_agent import BudgetCostAdvisorAgent
from agents.sustainability_material_advisor_agent import SustainabilityMaterialAdvisorAgent
from agents.client_preference_agent import ClientPreferenceAgent
from agents.competitor_insights_agent import CompetitorInsightsAgent

def test_budget_cost_advisor_agent_run(monkeypatch):
    agent = BudgetCostAdvisorAgent()
    monkeypatch.setattr(agent, "scrape_all_sites", lambda tags: [
        {"name": "Chair", "price": 100, "currency": "USD"},
        {"name": "Table", "price": 200, "currency": "USD"}
    ])
    monkeypatch.setattr(agent, "get_exchange_rates", lambda base: {"USD": 1.0})
    result = agent.run({"budget": 150, "style_tags": []})
    assert any(p["name"] == "Chair" for p in result["alternatives"])
    assert all(p["price"] <= 150 for p in result["alternatives"])

def test_sustainability_material_advisor_agent_run():
    agent = SustainabilityMaterialAdvisorAgent()
    result = agent.run({"material": "flooring"})
    assert "bamboo" in result["greener_alternatives"]
    assert isinstance(result["suppliers"], list)

def test_client_preference_agent_run():
    agent = ClientPreferenceAgent()
    survey = {"style_tags": ["modern"], "brands": ["IKEA"], "palette": ["blue"]}
    moodboard = [{"tag": "minimal"}]
    result = agent.run({"survey": survey, "moodboard": moodboard})
    assert "modern" in result["tags"] and "minimal" in result["tags"]
    assert "IKEA" in result["brands"]
    assert "blue" in result["palette"]

def test_competitor_insights_agent_run():
    agent = CompetitorInsightsAgent()
    result = agent.run({})
    assert "summary" in result

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main_agent import MainAgent
import pytest

def test_main_agent_routing(monkeypatch):
    agent = MainAgent()
    monkeypatch.setattr(agent.visualization_agent, "run", lambda t: {"visual": True})
    monkeypatch.setattr(agent.moodboard_agent, "run", lambda t: {"moodboard": True})
    monkeypatch.setattr(agent.furniture_advisor_agent, "run", lambda t: {"furniture": True})
    monkeypatch.setattr(agent.sustainability_advisor_agent, "run", lambda t: {"sustain": True})

    assert agent.route("visualization", {"prompt": "a"}) == {"visual": True}
    assert agent.route("visualization", {"moodboard": True}) == {"moodboard": True}
    assert agent.route("market", {"furniture": True}) == {"furniture": True}
    assert agent.route("sustainability", {}) == {"sustain": True}

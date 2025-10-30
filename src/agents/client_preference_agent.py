"""
ClientPreferenceAgent
- Profiles client preferences from surveys, mood boards, or Pinterest uploads.
- Builds a style fingerprint for use by other agents.
"""
from typing import Dict, Any

class ClientPreferenceAgent:
    def __init__(self):
        self.fingerprint = {}

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Example: extract style tags, color palette, brands from input
        survey = task.get("survey", {})
        moodboard = task.get("moodboard", [])
        pinterest = task.get("pinterest", [])
        tags = survey.get("style_tags", []) + [img.get("tag") for img in moodboard if "tag" in img]
        brands = survey.get("brands", [])
        palette = survey.get("palette", [])
        self.fingerprint = {"tags": tags, "brands": brands, "palette": palette}
        return self.fingerprint

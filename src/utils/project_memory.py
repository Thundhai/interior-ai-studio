"""
ProjectMemory
- Simple JSON-based project memory/context store (can be upgraded to SQLite).
"""
import json
import os
from typing import Any, Dict

class ProjectMemory:
    def __init__(self, path: str = "project_memory.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

    def load(self) -> Dict[str, Any]:
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data: Dict[str, Any]):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def update(self, project_id: str, update: Dict[str, Any]):
        data = self.load()
        if project_id not in data:
            data[project_id] = {}
        data[project_id].update(update)
        self.save(data)

    def get(self, project_id: str) -> Dict[str, Any]:
        data = self.load()
        return data.get(project_id, {})

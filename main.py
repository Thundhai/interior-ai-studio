# =========================
# LLM Provider Interface
# =========================
from typing import Optional, Any, Dict
import requests

class LLMProvider:
    """
    Base class for pluggable LLMs. Default: Ollama (local), with Replicate as optional.
    """
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

class OllamaLLM(LLMProvider):
    def __init__(self, model: str = "llama2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        # Example: call local Ollama API (http://localhost:11434)
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("response", "[No response]")
        except Exception as e:
            return f"[Ollama error: {e}]"

class ReplicateLLM(LLMProvider):
    def __init__(self, api_token: str, model: str = "meta/llama-2-70b-chat"):
        self.api_token = api_token
        self.model = model

    def generate(self, prompt: str) -> str:
        # Placeholder for Replicate API call
        return f"[Replicate LLM would generate text for: {prompt}]"

# =========================
# Image Generation Provider (Optional)
# =========================
class ImageGenerator:
    def generate(self, prompt: str) -> str:
        # Placeholder for Replicate or other image API
    """
    Modular image generator supporting Replicate (Stable Diffusion), OpenAI Images, or local ComfyUI.
    Set provider in __init__.
    """
    def __init__(self, provider: str = "replicate", api_token: str = "", endpoint: str = ""):
        self.provider = provider
        self.api_token = api_token
        self.endpoint = endpoint

    def generate(self, prompt: str, task: str = "rendering") -> str:
        if self.provider == "replicate":
            # Replicate Stable Diffusion API
            try:
                url = "https://api.replicate.com/v1/predictions"
                headers = {
                    "Authorization": f"Token {self.api_token}",
                    "Content-Type": "application/json"
                }
                # You can swap the model for moodboard, rendering, etc.
                model = "stability-ai/stable-diffusion"
                data = {
                    "version": "db21e45e1c1e6b6e8a6e3c7e3e8e3c7e3e8e3c7e3e8e3c7e",  # Example version
                    "input": {"prompt": prompt}
                }
                resp = requests.post(url, headers=headers, json=data, timeout=30)
                resp.raise_for_status()
                prediction = resp.json()
                # Replicate returns a URL to the generated image
                return prediction.get("urls", {}).get("get", "[No image URL]")
            except Exception as e:
                return f"[Replicate error: {e}]"
        elif self.provider == "openai":
            # OpenAI Images API (DALL-E)
            try:
                url = "https://api.openai.com/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
                data = {"prompt": prompt, "n": 1, "size": "1024x1024"}
                resp = requests.post(url, headers=headers, json=data, timeout=30)
                resp.raise_for_status()
                result = resp.json()
                return result["data"][0]["url"]
            except Exception as e:
                return f"[OpenAI error: {e}]"
        elif self.provider == "comfyui":
            # Local ComfyUI HTTP API (user must set endpoint)
            try:
                url = self.endpoint or "http://localhost:8188/generate"
                data = {"prompt": prompt, "task": task}
                resp = requests.post(url, json=data, timeout=30)
                resp.raise_for_status()
                result = resp.json()
                return result.get("image_url", "[No image URL]")
            except Exception as e:
                return f"[ComfyUI error: {e}]"
        else:
            return f"[Unknown image provider: {self.provider}]"
"""
AI Interior Design Studio - Multi-Agent System
Author: Babatunde 
Description: Starter architecture for AI agents to support luxury interior + exterior design workflow.
"""

import sys
from typing import Dict, Any
from .agents.visualization_agent import VisualizationAgent
from .agents.client_discovery_agent import ClientDiscoveryAgent
from .agents.style_inspiration_agent import StyleInspirationAgent
from .agents.space_planning_agent import SpacePlanningAgent
from .agents.material_sourcing_agent import MaterialSourcingAgent
from .agents.budget_estimation_agent import BudgetEstimationAgent
from .agents.project_management_agent import ProjectManagementAgent
from .agents.compliance_agent import ComplianceAgent
from .agents.feedback_revision_agent import FeedbackRevisionAgent
from .agents.client_presentation_agent import ClientPresentationAgent
from .agents.portfolio_marketing_agent import PortfolioMarketingAgent
from .agents.content_creator_agent import ContentCreatorAgent
from .agents.branding_identity_agent import BrandingIdentityAgent

# =========================
# Base Agent
# =========================
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclass with task-specific logic."""
        raise NotImplementedError


# =========================
# Agent Definitions
# =========================
class ClientDiscoveryAgent(BaseAgent):
    def run(self, input_data):
        return {"brief": f"Generated design brief from client preferences: {input_data}"}


class StyleInspirationAgent(BaseAgent):
    def run(self, input_data):
        return {"moodboard": f"Luxury style inspirations curated for: {input_data}"}


class SpacePlanningAgent(BaseAgent):
    def run(self, input_data):
        return {"layout": f"Space planning layout created for: {input_data}"}


class VisualizationAgent(BaseAgent):
    def run(self, input_data):
        # You can customize the prompt/task for moodboard, rendering, or mockup
        tasks = [
            ("moodboard", f"Create a luxury interior design moodboard for: {input_data}"),
            ("indoor_rendering", f"Photorealistic indoor rendering for: {input_data}"),
            ("outdoor_mockup", f"Outdoor architectural mockup for: {input_data}")
        ]
        results = {}
        for task, prompt in tasks:
            image_url = self.image_gen.generate(prompt, task=task)
            results[task] = image_url
        return results


class MaterialSourcingAgent(BaseAgent):
    def run(self, input_data):
        return {"sourcing": f"Suggested materials & vendors for: {input_data}"}


class BudgetEstimationAgent(BaseAgent):
    def run(self, input_data):
        return {"budget": f"Estimated costs breakdown for: {input_data}"}


class ProjectManagementAgent(BaseAgent):
    def run(self, input_data):
        return {"timeline": f"Project plan & milestones scheduled for: {input_data}"}


class ComplianceAgent(BaseAgent):
    def run(self, input_data):
        return {"compliance": f"Checked sustainability & compliance for: {input_data}"}


class FeedbackRevisionAgent(BaseAgent):
    def run(self, input_data):
        return {"revisions": f"Processed client feedback for: {input_data}"}


class ClientPresentationAgent(BaseAgent):
    def run(self, input_data):
        return {"presentation": f"Polished client presentation created for: {input_data}"}


class PortfolioMarketingAgent(BaseAgent):
    def run(self, input_data):
        return {"portfolio": f"Case study & social content prepared for: {input_data}"}


class ContentCreatorAgent(BaseAgent):
    def run(self, input_data):
        return {"content": f"Luxury design captions, blogs & visuals generated for: {input_data}"}


class BrandingIdentityAgent(BaseAgent):
    def run(self, input_data):
        return {"branding": f"Brand identity materials prepared for: {input_data}"}


# =========================
# Orchestrator / Root Agent
# =========================
class RootAgent:
    def __init__(self):
        self.agents = {
            "discovery": ClientDiscoveryAgent("Client Discovery"),
            "inspiration": StyleInspirationAgent("Style Inspiration"),
            "space": SpacePlanningAgent("Space Planning"),
            "visualization": VisualizationAgent("3D Visualization"),
            "sourcing": MaterialSourcingAgent("Material Sourcing"),
            "budget": BudgetEstimationAgent("Budget Estimation"),
            "management": ProjectManagementAgent("Project Management"),
            "compliance": ComplianceAgent("Compliance"),
            "feedback": FeedbackRevisionAgent("Feedback Revision"),
            "presentation": ClientPresentationAgent("Client Presentation"),
            "portfolio": PortfolioMarketingAgent("Portfolio & Marketing"),
            "content": ContentCreatorAgent("Content Creator"),
            "branding": BrandingIdentityAgent("Branding & Identity"),
        }

    def run_workflow(self, client_input: str):
        data = {"client_input": client_input}

        # Sequential pipeline (can be customized)
        workflow_order = [
            "discovery",
            "inspiration",
            "space",
            "visualization",
            "sourcing",
            "budget",
            "management",
            "compliance",
            "feedback",
            "presentation",
            "portfolio",
            "content",
            "branding",
        ]

        results = {}
        for step in workflow_order:
            agent = self.agents[step]
            output = agent.run(data)
            results[step] = output
            data.update(output)  # pass output to next agent

        return results


# =========================
# Run Example
# =========================
if __name__ == "__main__":
    root = RootAgent()
    project_input = "Luxury indoor-outdoor villa design with marble, glass, and smart lighting."
    results = root.run_workflow(project_input)

    print("\n=== Final Workflow Results ===")
    for step, output in results.items():
        print(f"{step.upper()}: {output}")

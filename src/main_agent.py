"""
MainAgent (Orchestrator)
- Routes tasks to sub-agents.
- Handles project context and memory (placeholder).
"""


from src.agents.visualization_agent import VisualizationAgent
from src.agents.content_creator_agent import ContentCreatorAgent
from src.agents.market_research_agent import MarketResearchAgent
from src.agents.style_advisor_agent import StyleAdvisorAgent
from src.agents.sustainability_advisor_agent import SustainabilityAdvisorAgent
from src.agents.furniture_advisor_agent import FurnitureAdvisorAgent
from src.agents.moodboard_agent import MoodBoardAgent
from src.agents.budget_cost_advisor_agent import BudgetCostAdvisorAgent
from src.agents.sustainability_material_advisor_agent import SustainabilityMaterialAdvisorAgent
from src.agents.client_preference_agent import ClientPreferenceAgent
from src.agents.competitor_insights_agent import CompetitorInsightsAgent
from src.utils.project_memory import ProjectMemory
from src.utils.knowledge_graph import KnowledgeGraphMemory
import argparse



class MainAgent:
    def __init__(self, memory_path: str = "project_memory.json", kg_uri=None, kg_user=None, kg_password=None):
        self.memory = ProjectMemory(memory_path)
        self.visualization_agent = VisualizationAgent()
        self.content_creator_agent = ContentCreatorAgent()
        self.market_research_agent = MarketResearchAgent()
        self.style_advisor_agent = StyleAdvisorAgent()
        self.sustainability_advisor_agent = SustainabilityAdvisorAgent()
        self.furniture_advisor_agent = FurnitureAdvisorAgent()
        self.moodboard_agent = MoodBoardAgent()
        self.budget_cost_advisor_agent = BudgetCostAdvisorAgent()
        self.sustainability_material_advisor_agent = SustainabilityMaterialAdvisorAgent()
        self.client_preference_agent = ClientPreferenceAgent()
        self.competitor_insights_agent = CompetitorInsightsAgent()
        self.knowledge_graph = KnowledgeGraphMemory(kg_uri, kg_user, kg_password)

    def add_product_to_kg(self, name, style, price, brand):
        return self.knowledge_graph.add_product(name, style, price, brand)

    def add_kg_relationship(self, from_label, from_name, to_label, to_name, rel_type):
        return self.knowledge_graph.add_relationship(from_label, from_name, to_label, to_name, rel_type)

    def query_kg(self, cypher):
        return self.knowledge_graph.query(cypher)

    def route(self, agent_name: str, task: dict, project_id: str = "default") -> dict:
        # Smarter routing based on agent_name and task
        result = None
        if agent_name == "visualization":
            if task.get("moodboard"):
                result = self.moodboard_agent.run(task)
                # Store tagged images in knowledge graph
                for img in result.get("images", []):
                    url = img.get("url")
                    tags = img.get("tags", [])
                    if url:
                        self.knowledge_graph.add_product(url, ",".join(tags), 0, "image")
            else:
                result = self.visualization_agent.run(task)
        elif agent_name == "content":
            result = self.content_creator_agent.run(task)
        elif agent_name == "market":
            if task.get("furniture"):
                result = self.furniture_advisor_agent.run(task)
            else:
                result = self.market_research_agent.run(task)
        elif agent_name == "style":
            result = self.style_advisor_agent.run(task)
        elif agent_name == "sustainability":
            result = self.sustainability_advisor_agent.run(task)
        elif agent_name == "budget":
            result = self.budget_cost_advisor_agent.run(task)
            # Store products in knowledge graph if available
            alternatives = result.get("alternatives", [])
            for product in alternatives:
                name = product.get("name")
                style = product.get("style", "")
                price = product.get("price", 0)
                brand = product.get("brand", "")
                if name:
                    self.add_product_to_kg(name, style, price, brand)
        elif agent_name == "material":
            result = self.sustainability_material_advisor_agent.run(task)
        elif agent_name == "client_preference":
            result = self.client_preference_agent.run(task)
        elif agent_name == "competitor_insights":
            result = self.competitor_insights_agent.run(task)
        else:
            return {"error": f"Agent '{agent_name}' not found."}
        self.memory.update(project_id, {agent_name: result})
        return result

    def get_project_context(self, project_id: str = "default"):
        return self.memory.get(project_id)


def main():
    parser = argparse.ArgumentParser(description="Interior AI Studio CLI")
    parser.add_argument("agent", type=str, help="Agent name (e.g. visualization, planner, budget, ...)")
    parser.add_argument("--project", type=str, default="default", help="Project ID")
    parser.add_argument("--prompt", type=str, help="Prompt or task description")
    parser.add_argument("--type", type=str, help="Task type (e.g. moodboard, rendering, etc.)")
    args = parser.parse_args()

    main_agent = MainAgent()
    task = {"prompt": args.prompt or "", "type": args.type or ""}
    result = main_agent.route(args.agent, task, project_id=args.project)
    print(f"{args.agent.capitalize()}Agent result:", result)
    print("\nProject context:", main_agent.get_project_context(args.project))

if __name__ == "__main__":
    main()

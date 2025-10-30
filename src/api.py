"""
FastAPI app for Interior AI Studio
- Exposes endpoints for each agent and project context
- Now includes endpoints for budget, material, client preference, and competitor insights agents.
"""
import os
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
from pydantic import BaseModel
from src.main_agent import MainAgent

app = FastAPI()
main_agent = MainAgent()

# CORS middleware for frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key authentication
API_KEY = os.getenv("INTERIOR_AI_API_KEY", "changeme")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

class AgentTask(BaseModel):
    project_id: str = "default"
    task: Dict[str, Any]


# Unified endpoint for all agent types
@app.post("/agent/{agent_name}")
def run_agent(agent_name: str, agent_task: AgentTask, x_api_key: str = Depends(verify_api_key)):
    result = main_agent.route(agent_name, agent_task.task, project_id=agent_task.project_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"result": result, "context": main_agent.get_project_context(agent_task.project_id)}

# Individual agent endpoints
@app.post("/budget")
def run_budget(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.budget_cost_advisor_agent.run(task)
    return {"result": result}

@app.post("/material")
def run_material(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.sustainability_material_advisor_agent.run(task)
    return {"result": result}

@app.post("/client_preference")
def run_client_preference(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.client_preference_agent.run(task)
    return {"result": result}

@app.post("/competitor_insights")
def run_competitor_insights(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.competitor_insights_agent.run(task)
    return {"result": result}

@app.post("/moodboard")
def run_moodboard(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.moodboard_agent.run(task)
    return {"result": result}

@app.post("/sustainability")
def run_sustainability(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    result = main_agent.sustainability_advisor_agent.run(task)
    return {"result": result}

# Export and knowledge graph endpoints
@app.post("/export_tagged_images")
def export_tagged_images(task: Dict[str, Any], x_api_key: str = Depends(verify_api_key)):
    """
    Exports tagged images for a given query using MoodBoardAgent. Returns the path to the exported JSON file.
    """
    result = main_agent.moodboard_agent.run(task)
    tagged_images = result.get("images", [])
    export_path = main_agent.moodboard_agent.export_tagged_images(tagged_images)
    return {"export_path": export_path}

@app.get("/download_tagged_images")
def download_tagged_images(export_path: str, x_api_key: str = Depends(verify_api_key)):
    """
    Download the exported tagged images JSON file for UI integration.
    """
    return FileResponse(export_path, media_type="application/json", filename="tagged_images.json")

@app.get("/graph_visualization")
def graph_visualization(x_api_key: str = Depends(verify_api_key)):
    """
    Visualize knowledge graph relationships for D3.js frontend.
    """
    cypher = '''
    MATCH (n)-[r]->(m)
    RETURN n, type(r) AS rel, m
    LIMIT 100
    '''
    results = main_agent.query_kg(cypher)
    # Format for D3.js: nodes and links
    nodes = {}
    links = []
    for row in results or []:
        n = row.get("n")
        m = row.get("m")
        rel = row.get("rel")
        if n:
            nodes[n.get("name", str(n))] = n
        if m:
            nodes[m.get("name", str(m))] = m
        if n and m and rel:
            links.append({"source": n.get("name", str(n)), "target": m.get("name", str(m)), "type": rel})
    return {"nodes": list(nodes.values()), "links": links}

@app.post("/smart_recommendations")
def smart_recommendations(preferences: dict, x_api_key: str = Depends(verify_api_key)):
    """
    Smart recommendations using knowledge graph with style, budget, sustainability filters.
    """
    style = preferences.get("style", "")
    budget = preferences.get("budget", 0)
    sustainability = preferences.get("sustainability", False)
    trending = preferences.get("trending", False)
    client_tags = preferences.get("client_tags", [])
    
    # Build Cypher query with all filters
    where_clauses = [f'p.style CONTAINS "{style}"', f'p.price <= {budget}']
    if sustainability:
        where_clauses.append('p.style CONTAINS "sustainable" OR p.tags CONTAINS "sustainable"')
    if trending:
        where_clauses.append('p.tags CONTAINS "trending"')
    for tag in client_tags:
        where_clauses.append(f'p.tags CONTAINS "{tag}"')
    where_str = " AND ".join(where_clauses)
    cypher = f'''
    MATCH (p:Product)
    WHERE {where_str}
    RETURN p.name AS name, p.style AS style, p.price AS price, p.brand AS brand
    '''
    results = main_agent.query_kg(cypher)
    return {"recommendations": results}

@app.post("/kg_query")
def kg_query(query: str, x_api_key: str = Depends(verify_api_key)):
    """
    Execute raw Cypher query on knowledge graph.
    """
    result = main_agent.query_kg(query)
    return {"result": result}

@app.get("/project/{project_id}")
def get_project_context(project_id: str, x_api_key: str = Depends(verify_api_key)):
    """
    Get project context and memory for a specific project.
    """
    return main_agent.get_project_context(project_id)

# Debug endpoints
@app.post("/debug/gemini_test")
def test_gemini_vision(image_url: str, x_api_key: str = Depends(verify_api_key)):
    """
    Test Gemini Vision API directly with a single image URL.
    Returns raw response for debugging.
    """
    try:
        tags = main_agent.moodboard_agent.call_clip_blip_model(image_url)
        return {
            "status": "success",
            "image_url": image_url,
            "tags": tags,
            "api_key_set": bool(main_agent.moodboard_agent.gemini_api_key)
        }
    except Exception as e:
        return {
            "status": "error",
            "image_url": image_url,
            "error": str(e),
            "api_key_set": bool(main_agent.moodboard_agent.gemini_api_key)
        }

# Interior AI Studio

# Interior AI Studio 🏠🤖

A sophisticated multi-agent AI system for luxury interior design, powered by 18 specialized agents and advanced knowledge graph technology.

## 🎯 Project Overview

Interior AI Studio is a comprehensive AI-powered design platform that combines:
- **Multi-agent orchestration** for specialized design tasks
- **Gemini Vision API integration** for intelligent image analysis
- **Knowledge graph technology** (Neo4j) for smart recommendations
- **FastAPI backend** with REST endpoints
- **Web scraping capabilities** for trend research and product sourcing

## 🤖 Available Agents

### Creative & Visualization
- **VisualizationAgent** - 2D/3D renders via Replicate Stable Diffusion
- **MoodBoardAgent** - Pinterest/Instagram scraping + AI image tagging
- **ContentCreatorAgent** - Marketing content generation

### Design & Style
- **StyleAdvisorAgent** - Trend analysis from fashion/lifestyle sites
- **TrendResearchAgent** - Design trend research
- **BrandingAgent** - Brand identity development

### Budget & Financial
- **BudgetCostAdvisorAgent** - IKEA/Wayfair/Houzz price scraping
- **BudgetEstimatorAgent** - Project cost estimation

### Sustainability
- **SustainabilityAdvisorAgent** - Eco-friendly recommendations
- **SustainabilityMaterialAdvisorAgent** - Green materials sourcing

### Furniture & Materials
- **FurnitureAdvisorAgent** - Furniture recommendations
- **MaterialSourcingAgent** - Material supplier sourcing

### Research & Analysis
- **MarketResearchAgent** - Houzz/Dezeen trend analysis
- **CompetitorInsightsAgent** - Competitor analysis

### Client & Communication
- **ClientPreferenceAgent** - Style profiling from surveys/moodboards
- **ClientCommunicationAgent** - Project communication management

### Project Management
- **ProjectPlannerAgent** - Timeline and project management
- **MainAgent** - Orchestrates all agents and knowledge graph

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/interior-ai-studio.git
cd interior-ai-studio

# Install dependencies
pip install -r requirements.txt

# Run the test suite (works without external APIs)
python test_agents.py
```

### API Key Setup (Optional)
For full functionality, set these environment variables:
```bash
# Gemini Vision API
export GEMINI_API_KEY="your-gemini-api-key"

# Replicate API (for image generation)
export REPLICATE_API_TOKEN="your-replicate-token"

# Interior AI API Key (for security)
export INTERIOR_AI_API_KEY="changeme"
```

### Running the Server
```bash
# Option 1: Direct agent testing (recommended for demo)
python test_agents.py

# Option 2: Full API server (requires setup)
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## 📊 Demo Results

```
🚀 Testing Interior AI Studio Agents...

1️⃣ Testing MoodBoard Agent...
✅ MoodBoard result: Images scraped and tagged

2️⃣ Testing Gemini Vision API...
✅ Fallback tags: ['modern', 'minimal', 'bright']

3️⃣ Testing Style Advisor Agent...
✅ Style advisor result: Trends analyzed

4️⃣ Testing Budget Cost Advisor Agent...
✅ Budget advisor result: Alternatives found

🎉 All agents tested successfully!
```

## 🏗️ Architecture

```
interior-ai-studio/
├── src/
│   ├── agents/           # 18 specialized AI agents
│   ├── utils/            # Knowledge graph & memory
│   ├── api.py           # FastAPI REST endpoints
│   └── main_agent.py    # Orchestrator
├── ui/                  # Sample frontend
├── tests/               # Test suites
└── test_agents.py       # Direct agent testing
```

## 🔌 API Endpoints

- `POST /moodboard` - Generate AI-tagged moodboards
- `POST /smart_recommendations` - Knowledge graph recommendations
- `POST /export_tagged_images` - Export tagged images as JSON
- `GET /graph_visualization` - D3.js-ready graph data
- `POST /debug/gemini_test` - Test Gemini Vision integration
- `GET /docs` - Interactive API documentation

## 🔮 Key Features

### ✅ Implemented
- [x] Multi-agent orchestration system
- [x] Gemini Vision API integration (auth setup needed)
- [x] Knowledge graph with Neo4j
- [x] Web scraping for trends/products
- [x] Smart recommendation engine
- [x] Export/import functionality
- [x] REST API with 15+ endpoints
- [x] Comprehensive test suite

### 🚧 In Progress
- [ ] Production deployment configuration
- [ ] Google Cloud authentication setup
- [ ] Enhanced UI/UX components

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, Neo4j
- **AI/ML**: Gemini Vision API, Replicate API
- **Data**: Web scraping (BeautifulSoup), Knowledge Graphs
- **Testing**: Pytest, Direct agent testing
- **Deployment**: Docker-ready, Cloud-compatible

## 📈 Performance & Scale

- **18 specialized agents** working in coordination
- **Knowledge graph** for intelligent recommendations
- **Caching system** for improved performance
- **Modular architecture** for easy scaling

## 🤝 Contributing

This is a professional AI system designed for luxury interior design. The modular architecture allows for easy extension and customization.

## 📄 License

Private project - All rights reserved.

---

**Built with 🏠 for the future of interior design**

## Features
- Visualization, planning, budgeting, sourcing, content, branding, communication, and trend research agents
- Orchestrator (MainAgent) for routing and project context
- Pluggable LLM and image generation (Ollama, OpenAI, Replicate, ComfyUI)
- CLI-first, FastAPI-ready

## Setup
1. `pip install -r requirements.txt`
2. Add API keys to `.env`
3. Run agents via CLI or extend with FastAPI


## Usage

### CLI Example
```sh
python -m src.main_agent visualization --prompt "Modern luxury living room with marble and gold accents." --type moodboard --project demo1
```

### FastAPI Example
Start the server:
```sh
uvicorn src.api:app --reload
```
Then POST to `/agent/visualization` with:
```json
{
	"project_id": "demo1",
	"task": {
		"prompt": "Modern luxury living room with marble and gold accents.",
		"type": "moodboard"
	}
}
```
Include header: `x-api-key: changeme` (or your key)

### API Docs
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Agents
- **VisualizationAgent**: Generates 2D/3D renders, moodboards, suggests materials/colors (Replicate Stable Diffusion)
- **ProjectPlannerAgent**: Manages timelines, checklists, Gantt charts
- **BudgetEstimatorAgent**: Material cost breakdowns, luxury/cost-saving options
- **MaterialSourcingAgent**: Supplier lookup, lead time estimates
- **ContentCreatorAgent**: Blogs, social posts, SEO, OpenAI GPT integration
- **BrandingAgent**: Brand voice, proposals, taglines
- **ClientCommunicationAgent**: Emails, presentations, progress summaries
- **TrendResearchAgent**: Monitors trends, luxury recommendations

## Testing
Run all tests:
```sh
pytest tests/
```

## Auth
Set `INTERIOR_AI_API_KEY` in `.env` and use `x-api-key` header for all API requests.

## Attribution
See `CLAUDE.md` for AI assistance acknowledgment.

# Interior AI Studio - GitHub Deployment

## 🚀 Quick Client Demo

Your client can run this immediately without any setup:

```bash
git clone https://github.com/yourusername/interior-ai-studio.git
cd interior-ai-studio
pip install -r requirements.txt
python demo.py
```

## 🏗️ For Full Production Deployment

### Option 1: Docker (Recommended)
```bash
# Set your API keys
export GEMINI_API_KEY="your-key"
export REPLICATE_API_TOKEN="your-token"

# Deploy with Docker Compose
docker-compose up -d

# Access at http://localhost:8000/docs
```

### Option 2: Manual Server Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-gemini-key"
export REPLICATE_API_TOKEN="your-replicate-token"
export INTERIOR_AI_API_KEY="secure-api-key"

# Run server
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### Option 3: Cloud Deployment

#### Heroku
```bash
heroku create interior-ai-studio
heroku config:set GEMINI_API_KEY="your-key"
heroku config:set REPLICATE_API_TOKEN="your-token"
git push heroku main
```

#### AWS/GCP/Azure
- Use the included Dockerfile
- Set environment variables in your cloud console
- Deploy container to your preferred cloud service

## 🔑 Required API Keys

1. **Gemini Vision API** (Google Cloud)
   - Enable Vision API in Google Cloud Console
   - Create service account or API key
   - Set `GEMINI_API_KEY` environment variable

2. **Replicate API** (Optional - for image generation)
   - Sign up at replicate.com
   - Get API token from dashboard
   - Set `REPLICATE_API_TOKEN` environment variable

3. **Neo4j** (Optional - for knowledge graph)
   - Use Neo4j Aura (cloud) or local installation
   - Set `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`

## 📊 API Documentation

Once deployed, visit `/docs` for interactive API documentation.

Key endpoints:
- `POST /moodboard` - Generate mood boards
- `POST /smart_recommendations` - AI recommendations
- `GET /graph_visualization` - Knowledge graph data
- `POST /debug/gemini_test` - Test AI integration

## 🎯 Client Integration

Your Firestore frontend can connect by updating API URLs:
```javascript
const API_BASE = "https://your-deployed-url.com";
// or "http://localhost:8000" for local testing

fetch(`${API_BASE}/moodboard`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'changeme'
  },
  body: JSON.stringify({query: "modern living room"})
});
```
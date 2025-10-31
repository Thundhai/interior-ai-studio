# 🌊 RENDER DEPLOYMENT - PROFESSIONAL OPTION

## Deploy to Render (10 minutes to live link)

### 1. **Go to Render**
```bash
https://render.com
```

### 2. **Create Web Service**
- Click "New +" → "Web Service"
- Connect GitHub: `Thundhai/interior-ai-studio`
- Render auto-detects Python

### 3. **Configuration**
```yaml
Name: interior-ai-studio
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

### 4. **Environment Variables**
```bash
PYTHONPATH=/app
INTERIOR_AI_API_KEY=your-secure-key
GEMINI_API_KEY=your-gemini-key
```

### 5. **Deploy**
- Render builds and deploys automatically
- Professional URL: `https://interior-ai-studio.onrender.com`

### 6. **Your Live Links**
```bash
https://interior-ai-studio.onrender.com/docs      # Interactive API docs
https://interior-ai-studio.onrender.com/agents    # Agent showcase
https://interior-ai-studio.onrender.com/redoc     # Documentation
```

**Cost**: FREE tier available
**Time**: 10-15 minutes  
**URL**: Professional .onrender.com domain
**Features**: Auto-deploy, SSL, monitoring
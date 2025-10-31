# ☁️ GOOGLE CLOUD RUN - ENTERPRISE OPTION

## Deploy to Google Cloud Run (15 minutes to live link)

### 1. **Enable Cloud Run**
```bash
https://console.cloud.google.com/run
```

### 2. **Deploy from Source**
- Click "Create Service" 
- Select "Deploy from source repository"
- Connect GitHub: `Thundhai/interior-ai-studio`

### 3. **Configuration**
```yaml
Service Name: interior-ai-studio
Region: us-central1 (or nearest)
Container Port: 8000
Memory: 1 GiB
CPU: 1
```

### 4. **Environment Variables**
```bash
PYTHONPATH=/app
INTERIOR_AI_API_KEY=your-secure-key
GEMINI_API_KEY=your-gemini-key
PORT=8000
```

### 5. **Deploy**
- Google builds container and deploys
- Enterprise URL: `https://interior-ai-studio-xyz.run.app`

### 6. **Your Live Links**
```bash
https://interior-ai-studio-xyz.run.app/docs       # API Documentation
https://interior-ai-studio-xyz.run.app/agents     # Agent showcase  
https://interior-ai-studio-xyz.run.app/redoc      # Alternative docs
```

**Cost**: Pay-per-use (very affordable)
**Time**: 15-20 minutes
**URL**: Professional .run.app domain  
**Features**: Auto-scaling, enterprise security, 99.9% uptime
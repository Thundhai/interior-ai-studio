#!/usr/bin/env python3
"""
Production startup script for Interior AI Studio
Ensures all dependencies are available and starts the FastAPI server
"""
import os
import sys

def main():
    """Start the Interior AI Studio API server"""
    try:
        # Set Python path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import and start the API
        import uvicorn
        from src.api import app
        
        # Get port from environment (Railway, Render, etc. set this)
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")
        
        print(f"🚀 Starting Interior AI Studio on {host}:{port}")
        print(f"📚 API docs will be available at: http://{host}:{port}/docs")
        print(f"🤖 Agent list at: http://{host}:{port}/agents")
        
        # Start the server
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
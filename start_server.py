#!/usr/bin/env python3
"""
Production startup script for Interior AI Studio
Handles Railway's PORT environment variable correctly
"""
import os
import sys

def main():
    """Start the Interior AI Studio API server with correct PORT handling"""
    try:
        # Set Python path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Get port from Railway's PORT environment variable
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        print(f"🚀 Starting Interior AI Studio for Railway")
        print(f"🌐 Server will listen on {host}:{port}")
        print(f"� PORT environment variable: {os.environ.get('PORT', 'not set, using default 8000')}")
        print(f"📚 Health check endpoint: http://{host}:{port}/")
        print(f"🤖 Agent list endpoint: http://{host}:{port}/agents")
        print(f"📖 API docs: http://{host}:{port}/docs")
        
        # Import and start the API
        import uvicorn
        from src.api import app
        
        # Start the server with Railway's configuration
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
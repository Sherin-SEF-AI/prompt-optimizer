#!/usr/bin/env python3
"""
Start script for the Enhanced LLM Prompt Optimizer API Server.
This script provides an easy way to start the API server with proper configuration.
"""

import os
import sys
import uvicorn
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sqlalchemy
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_environment():
    """Check and set up environment variables."""
    print("🔧 Checking environment configuration...")
    
    # Set default values if not present
    if not os.getenv("LOG_LEVEL"):
        os.environ["LOG_LEVEL"] = "INFO"
        print("   Set LOG_LEVEL=INFO")
    
    if not os.getenv("DATABASE_URL"):
        os.environ["DATABASE_URL"] = "sqlite:///prompt_optimizer.db"
        print("   Set DATABASE_URL=sqlite:///prompt_optimizer.db")
    
    print("✅ Environment configured")

def start_server():
    """Start the API server."""
    print("🚀 Starting Enhanced LLM Prompt Optimizer API Server...")
    print("=" * 60)
    
    # Import and create the app
    try:
        from prompt_optimizer.api.server import create_app
        app = create_app()
        print("✅ API server created successfully")
    except Exception as e:
        print(f"❌ Failed to create API server: {e}")
        return False
    
    # Server configuration
    host = "0.0.0.0"
    port = 8000
    reload = True  # Enable auto-reload for development
    
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"📖 Alternative docs: http://{host}:{port}/redoc")
    print("=" * 60)
    print("🔄 Starting server... (Press Ctrl+C to stop)")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False

def main():
    """Main function to start the API server."""
    print("🎯 Enhanced LLM Prompt Optimizer API Server")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("prompt_optimizer").exists():
        print("❌ Please run this script from the project root directory")
        print("   Current directory should contain the 'prompt_optimizer' folder")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check environment
    check_environment()
    
    # Start server
    return start_server()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
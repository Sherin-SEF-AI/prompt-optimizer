"""
Main entry point for RapidAPI deployment.
"""

import os
from prompt_optimizer.api.server import create_app
from prompt_optimizer.types import OptimizerConfig

# Load configuration from environment variables
config = OptimizerConfig(
    api_keys={
        "openai": os.getenv("OPENAI_API_KEY", ""),
        "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
        "google": os.getenv("GOOGLE_API_KEY", ""),
    },
    database_url=os.getenv("DATABASE_URL", "sqlite:///prompt_optimizer.db"),
    redis_url=os.getenv("REDIS_URL"),
    log_level=os.getenv("LOG_LEVEL", "INFO")
)

# Create FastAPI app
app = create_app(config)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

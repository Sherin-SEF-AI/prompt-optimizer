#!/usr/bin/env python3
"""
RapidAPI Deployment Script for LLM Prompt Optimizer

This script helps set up and deploy the LLM Prompt Optimizer API to RapidAPI.
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load RapidAPI configuration from YAML file."""
    config_path = Path("rapidapi_config.yaml")
    if not config_path.exists():
        print("❌ rapidapi_config.yaml not found!")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def check_prerequisites() -> bool:
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    if not Path("prompt_optimizer").exists():
        print("❌ prompt_optimizer directory not found!")
        return False
    
    # Check if API server exists
    if not Path("prompt_optimizer/api/server.py").exists():
        print("❌ API server not found!")
        return False
    
    # Check if requirements file exists
    if not Path("requirements_rapidapi.txt").exists():
        print("❌ requirements_rapidapi.txt not found!")
        return False
    
    # Check if Dockerfile exists
    if not Path("Dockerfile.rapidapi").exists():
        print("❌ Dockerfile.rapidapi not found!")
        return False
    
    print("✅ All prerequisites met!")
    return True

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate the RapidAPI configuration."""
    print("🔍 Validating configuration...")
    
    required_fields = [
        "api.name",
        "api.description", 
        "api.version",
        "authentication.type",
        "endpoints.base_url"
    ]
    
    for field in required_fields:
        keys = field.split('.')
        value = config
        for key in keys:
            if key not in value:
                print(f"❌ Missing required field: {field}")
                return False
            value = value[key]
    
    print("✅ Configuration is valid!")
    return True

def create_deployment_files(config: Dict[str, Any]) -> None:
    """Create deployment-specific files."""
    print("📝 Creating deployment files...")
    
    # Create main.py for deployment
    main_content = '''"""
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
'''
    
    with open("main.py", "w") as f:
        f.write(main_content)
    
    print("✅ Created main.py")

def create_rapidapi_json(config: Dict[str, Any]) -> None:
    """Create RapidAPI-specific configuration JSON."""
    print("📝 Creating RapidAPI configuration...")
    
    rapidapi_config = {
        "name": config["api"]["name"],
        "description": config["api"]["description"],
        "version": config["api"]["version"],
        "category": config["api"]["category"],
        "tags": config["api"]["tags"],
        "authentication": {
            "type": config["authentication"]["type"],
            "header_name": config["authentication"]["header_name"]
        },
        "endpoints": {
            "base_url": config["endpoints"]["base_url"],
            "health_check": config["endpoints"]["health_check"]
        },
        "pricing": config["pricing"],
        "deployment": config["deployment"]
    }
    
    with open("rapidapi.json", "w") as f:
        json.dump(rapidapi_config, f, indent=2)
    
    print("✅ Created rapidapi.json")

def create_readme_rapidapi(config: Dict[str, Any]) -> None:
    """Create RapidAPI-specific README."""
    print("📝 Creating RapidAPI README...")
    
    readme_content = f"""# {config['api']['name']} - RapidAPI

{config['api']['description']}

## Quick Start

### 1. Subscribe to the API
Visit the [RapidAPI marketplace](https://rapidapi.com) and subscribe to the {config['api']['name']} API.

### 2. Get Your API Key
After subscribing, you'll receive your RapidAPI key.

### 3. Make Your First Request

```bash
curl --request GET \\
  --url {config['endpoints']['base_url']}/health \\
  --header 'X-RapidAPI-Key: YOUR_API_KEY' \\
  --header 'X-RapidAPI-Host: llm-prompt-optimizer.p.rapidapi.com'
```

## API Documentation

- **Interactive Docs**: {config['endpoints']['base_url']}/docs
- **OpenAPI Spec**: {config['endpoints']['base_url']}/openapi.json
- **GitHub**: {config['documentation']['github']}
- **PyPI**: {config['documentation']['pypi']}

## Support

- **Email**: {config['support']['email']}
- **GitHub Issues**: {config['support']['github_issues']}
- **Documentation**: {config['support']['documentation']}

## License

{config['legal']['license']} License - see {config['legal']['terms_of_service']} for details.
"""
    
    with open("README_RAPIDAPI.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README_RAPIDAPI.md")

def run_tests() -> bool:
    """Run basic tests to ensure the API works."""
    print("🧪 Running basic tests...")
    
    try:
        # Test if the server can be imported
        from prompt_optimizer.api.server import create_app
        from prompt_optimizer.types import OptimizerConfig
        
        # Create a test app
        config = OptimizerConfig()
        app = create_app(config)
        
        print("✅ Server imports successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main deployment script."""
    print("🚀 RapidAPI Deployment Script for LLM Prompt Optimizer")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but continuing with deployment...")
    
    # Create deployment files
    create_deployment_files(config)
    create_rapidapi_json(config)
    create_readme_rapidapi(config)
    
    print("\n🎉 Deployment files created successfully!")
    print("\n📋 Next steps:")
    print("1. Review the generated files:")
    print("   - main.py")
    print("   - rapidapi.json") 
    print("   - README_RAPIDAPI.md")
    print("2. Push your code to GitHub")
    print("3. Connect your repository to RapidAPI Hub")
    print("4. Configure environment variables in RapidAPI")
    print("5. Deploy your API")
    print("\n📚 For detailed instructions, see: rapidapi_deployment.md")

if __name__ == "__main__":
    main() 
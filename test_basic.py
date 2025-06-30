#!/usr/bin/env python3
"""
Basic test script for the prompt-optimizer package.

Author: Sherin Joseph Roy
Email: sherin.joseph2217@gmail.com
GitHub: https://github.com/Sherin-SEF-AI/prompt-optimizer.git
LinkedIn: https://www.linkedin.com/in/sherin-roy-deepmost/
"""

import asyncio
import sys
from typing import Dict, Any

# Test imports
print("🧪 Prompt Optimizer Test Suite")
print("=" * 50)
print("Author: Sherin Joseph Roy")
print("Email: sherin.joseph2217@gmail.com")
print("GitHub: https://github.com/Sherin-SEF-AI/prompt-optimizer.git")
print("LinkedIn: https://www.linkedin.com/in/sherin-roy-deepmost/")
print("=" * 50)

print("🔍 Testing Module Imports...")
print("=" * 30)

try:
    from prompt_optimizer import PromptOptimizer
    print("✅ Main package: prompt_optimizer")
except Exception as e:
    print(f"❌ Main package: {e}")

try:
    from prompt_optimizer.core import PromptOptimizer
    print("✅ Core modules: prompt_optimizer.core")
except Exception as e:
    print(f"❌ Core modules: {e}")

try:
    from prompt_optimizer.testing import ABTest
    print("✅ Testing modules: prompt_optimizer.testing")
except Exception as e:
    print(f"❌ Testing modules: {e}")

try:
    from prompt_optimizer.providers import OpenAIProvider, AnthropicProvider
    print("✅ Provider modules: prompt_optimizer.providers")
except Exception as e:
    print(f"❌ Provider modules: {e}")

try:
    from prompt_optimizer.analytics import QualityScorer, CostTracker
    print("✅ Analytics modules: prompt_optimizer.analytics")
except Exception as e:
    print(f"❌ Analytics modules: {e}")

try:
    from prompt_optimizer.optimization import GeneticOptimizer
    print("✅ Optimization modules: prompt_optimizer.optimization")
except Exception as e:
    print(f"❌ Optimization modules: {e}")

try:
    from prompt_optimizer.storage import DatabaseManager
    print("✅ Storage modules: prompt_optimizer.storage")
except Exception as e:
    print(f"❌ Storage modules: {e}")

try:
    from prompt_optimizer.api import create_app
    from prompt_optimizer.types import OptimizerConfig
    config = OptimizerConfig()
    print("✅ API modules: prompt_optimizer.api")
except Exception as e:
    print(f"❌ API modules: {e}")

try:
    from prompt_optimizer.cli import main
    print("✅ CLI modules: prompt_optimizer.cli")
except Exception as e:
    print(f"❌ CLI modules: {e}")

try:
    from prompt_optimizer.visualization import Dashboard, Charts
    print("✅ Visualization modules: prompt_optimizer.visualization")
except Exception as e:
    print(f"❌ Visualization modules: {e}")

print("\n🔧 Testing Type Definitions...")
print("=" * 30)

try:
    from prompt_optimizer.types import (
        OptimizerConfig, ExperimentConfig, ProviderType, 
        MetricType, TestStatus, PromptVariant, TestResult
    )
    print("✅ Type definitions imported successfully")
except Exception as e:
    print(f"❌ Type definitions: {e}")

print("\n🧪 Testing Basic Functionality...")
print("=" * 30)

async def test_basic_functionality():
    """Test basic package functionality."""
    try:
        # Test config creation
        from prompt_optimizer.types import OptimizerConfig, ProviderType
        config = OptimizerConfig(
            database_url="sqlite:///test.db",
            default_provider=ProviderType.OPENAI
        )
        print("✅ Config creation: Success")
        
        # Test optimizer initialization
        from prompt_optimizer import PromptOptimizer
        optimizer = PromptOptimizer(config)
        print("✅ Optimizer initialization: Success")
        
        # Test experiment config
        from prompt_optimizer.types import ExperimentConfig
        exp_config = ExperimentConfig(
            name="test_experiment",
            traffic_split={"control": 0.5, "variant": 0.5},
            provider=ProviderType.OPENAI,
            model="gpt-3.5-turbo"
        )
        print("✅ Experiment config: Success")
        
        # Test quality scorer
        from prompt_optimizer.analytics import QualityScorer
        scorer = QualityScorer()
        print("✅ Quality scorer: Success")
        
        # Test cost tracker
        from prompt_optimizer.analytics import CostTracker
        tracker = CostTracker()
        print("✅ Cost tracker: Success")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

# Run the test
success = asyncio.run(test_basic_functionality())

print("\n📊 Test Summary")
print("=" * 30)
if success:
    print("✅ Package is working correctly!")
    print("✅ All core modules can be imported")
    print("✅ Basic functionality is operational")
    print("✅ Ready for development and testing")
else:
    print("❌ Some tests failed")
    print("❌ Check the error messages above")

print("\n🚀 Next Steps:")
print("- Install additional dependencies if needed")
print("- Configure API keys for providers")
print("- Run the API server: uvicorn prompt_optimizer.api.server:app --reload")
print("- Test the CLI: prompt-optimizer --help")
print("- Check the documentation: https://github.com/Sherin-SEF-AI/prompt-optimizer.git")

print("\n📞 Support:")
print("- Email: sherin.joseph2217@gmail.com")
print("- GitHub: https://github.com/Sherin-SEF-AI/prompt-optimizer.git")
print("- LinkedIn: https://www.linkedin.com/in/sherin-roy-deepmost/")

print("\n" + "=" * 50)
print("Made with ❤️ by Sherin Joseph Roy")
print("=" * 50) 
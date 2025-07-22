# 🚀 Enhanced LLM Prompt Optimizer API

A comprehensive, enterprise-ready API for systematic A/B testing and optimization of LLM prompts with advanced analytics, monitoring, and security features.

## ✨ Features

### 🧪 Core Functionality
- **A/B Testing**: Create and run experiments with multiple prompt variants
- **Prompt Optimization**: Use genetic algorithms to optimize prompts
- **Multi-Provider Support**: Works with OpenAI, Anthropic, Google, and more
- **Statistical Analysis**: Calculate significance and confidence intervals

### 📊 Analytics & Monitoring
- **Cost Tracking**: Monitor API costs and token usage
- **Quality Scoring**: Automated quality assessment of responses
- **Performance Analytics**: System metrics and performance monitoring
- **Predictive Analytics**: Forecasting and trend analysis
- **Real-time Dashboards**: Live monitoring and visualizations

### 🔒 Security & Compliance
- **Content Moderation**: Safety and compliance checking
- **Bias Detection**: Identify and flag biased content
- **Injection Detection**: Prevent prompt injection attacks
- **Audit Logging**: Comprehensive security audit trails
- **Compliance Checking**: Verify experiment compliance

### 📈 Advanced Testing
- **Statistical Significance**: Calculate p-values and effect sizes
- **A/B Test Runner**: Automated test execution
- **Export Capabilities**: CSV and JSON export options
- **Report Generation**: Comprehensive analytics reports

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
# Easy start script
python3 start_api_server.py

# Or directly
python3 prompt_optimizer/api/server.py
```

### 3. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📋 API Endpoints Overview

### Health & Information
- `GET /` - API information and documentation
- `GET /health` - Health check

### Experiment Management
- `POST /api/v1/experiments` - Create experiments
- `GET /api/v1/experiments` - List experiments
- `GET /api/v1/experiments/{id}` - Get experiment details
- `POST /api/v1/experiments/{id}/start` - Start experiment
- `POST /api/v1/experiments/{id}/stop` - Stop experiment

### Testing & Results
- `POST /api/v1/test` - Test prompts
- `GET /api/v1/experiments/{id}/results` - Get results
- `GET /api/v1/experiments/{id}/analyze` - Analyze experiment
- `GET /api/v1/experiments/{id}/export` - Export results

### Analytics
- `GET /api/v1/analytics/cost-summary` - Cost tracking
- `GET /api/v1/analytics/quality-report` - Quality metrics
- `GET /api/v1/analytics/generate-report` - Generate reports
- `GET /api/v1/analytics/predictive` - Predictive analytics

### Monitoring
- `GET /api/v1/monitoring/dashboard` - Real-time dashboard
- `GET /api/v1/monitoring/metrics` - System metrics

### Security
- `POST /api/v1/security/check-content` - Content safety
- `POST /api/v1/security/detect-bias` - Bias detection
- `POST /api/v1/security/check-injection` - Injection detection
- `GET /api/v1/security/audit-logs` - Audit logs
- `POST /api/v1/security/compliance-check` - Compliance check

### Testing & Statistical
- `POST /api/v1/testing/ab-test` - Run A/B tests
- `GET /api/v1/testing/significance` - Calculate significance

### Optimization
- `POST /api/v1/optimize` - Optimize prompts

### Configuration
- `GET /api/v1/config` - Get configuration

## 💡 Usage Examples

### Create an A/B Test Experiment
```python
import requests

# Create experiment
response = requests.post("http://localhost:8000/api/v1/experiments", json={
    "name": "Customer Support Test",
    "description": "Testing different customer support prompt styles",
    "variants": [
        {
            "name": "friendly",
            "template": "Hi there! I'm here to help you with: {input}",
            "parameters": {}
        },
        {
            "name": "professional",
            "template": "Thank you for contacting us. Regarding: {input}",
            "parameters": {}
        }
    ],
    "config": {
        "traffic_split": 0.5,
        "min_sample_size": 100,
        "confidence_level": 0.95
    }
})

experiment_id = response.json()["data"]["experiment_id"]
print(f"Created experiment: {experiment_id}")
```

### Test a Prompt
```python
# Test the prompt
test_response = requests.post("http://localhost:8000/api/v1/test", json={
    "experiment_id": experiment_id,
    "user_id": "user_123",
    "input_data": {
        "question": "I need help with my order"
    }
})

result = test_response.json()
print(f"Variant used: {result['data']['variant_name']}")
print(f"Response: {result['data']['response']}")
print(f"Quality score: {result['data']['quality_score']}")
```

### Analyze Results
```python
# Analyze the experiment
analysis = requests.get(f"http://localhost:8000/api/v1/experiments/{experiment_id}/analyze")
report = analysis.json()

print(f"Best variant: {report['data']['best_variant']}")
print(f"Confidence level: {report['data']['confidence_level']}")
print(f"Total samples: {report['data']['total_samples']}")
```

### Check Content Safety
```python
# Check content for safety
safety_check = requests.post("http://localhost:8000/api/v1/security/check-content", json={
    "content": "This is a test message to check for safety and compliance."
})

safety_result = safety_check.json()
print(f"Safety score: {safety_result['data']['safety_score']}")
print(f"Is safe: {safety_result['data']['is_safe']}")
```

## 🧪 Testing the API

### Run the Test Suite
```bash
# Run comprehensive tests
python3 test_all_features.py

# Test the API endpoints
python3 test_enhanced_api.py
```

### Manual Testing
1. Start the server: `python3 start_api_server.py`
2. Open http://localhost:8000/docs in your browser
3. Try the interactive API documentation
4. Test endpoints directly from the Swagger UI

## 📊 Monitoring & Analytics

### Real-time Dashboard
Access the dashboard at: `GET /api/v1/monitoring/dashboard`

Returns:
- Active experiments count
- Total API calls
- Average response times
- Cost metrics
- Quality scores

### Cost Tracking
```python
# Get cost summary
costs = requests.get("http://localhost:8000/api/v1/analytics/cost-summary")
cost_data = costs.json()

print(f"Total cost: ${cost_data['data']['total_cost']}")
print(f"Cost this month: ${cost_data['data']['monthly_cost']}")
print(f"Average cost per request: ${cost_data['data']['avg_cost_per_request']}")
```

## 🔒 Security Features

### Content Safety Check
```python
safety = requests.post("http://localhost:8000/api/v1/security/check-content", json={
    "content": "Your content here"
})
```

### Bias Detection
```python
bias = requests.post("http://localhost:8000/api/v1/security/detect-bias", json={
    "text": "Text to check for bias"
})
```

### Injection Attack Detection
```python
injection = requests.post("http://localhost:8000/api/v1/security/check-injection", json={
    "prompt": "Prompt to check for injection attacks"
})
```

## 🚀 Deployment

### Local Development
```bash
python3 start_api_server.py
```

### Production Deployment
```bash
# Using Docker
docker build -f Dockerfile.rapidapi -t prompt-optimizer-api .
docker run -p 8000:8000 prompt-optimizer-api

# Using uvicorn directly
uvicorn prompt_optimizer.api.server:app --host 0.0.0.0 --port 8000
```

### RapidAPI Deployment
```bash
python3 deploy_rapidapi.py
```

## 📚 Documentation

- **Complete API Reference**: `API_ENDPOINTS.md`
- **Enhancement Summary**: `ENHANCEMENT_SUMMARY.md`
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DATABASE_URL="sqlite:///prompt_optimizer.db"
export LOG_LEVEL="INFO"
```

### API Configuration
```python
from prompt_optimizer.types import OptimizerConfig

config = OptimizerConfig(
    api_keys={
        "openai": "your-key",
        "anthropic": "your-key"
    },
    database_url="sqlite:///prompt_optimizer.db",
    max_concurrent_tests=10,
    cache_ttl=3600
)
```

## 🎯 Use Cases

### E-commerce
- A/B test product recommendation prompts
- Optimize customer support responses
- Test different marketing copy

### SaaS Applications
- Optimize onboarding flows
- Test feature explanation prompts
- Improve user engagement

### Content Creation
- Test different writing styles
- Optimize content generation prompts
- A/B test creative directions

### Customer Support
- Test response templates
- Optimize resolution times
- Improve customer satisfaction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Email**: sherin.joseph2217@gmail.com
- **GitHub**: https://github.com/Sherin-SEF-AI/prompt-optimizer.git
- **Documentation**: http://localhost:8000/docs

---

**The Enhanced LLM Prompt Optimizer API is ready for production use! 🚀** 
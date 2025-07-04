# RapidAPI Deployment Guide for LLM Prompt Optimizer

## Overview

This guide will help you deploy the LLM Prompt Optimizer API to RapidAPI, making it available as a marketplace API for developers worldwide.

## Prerequisites

1. **RapidAPI Account**: Sign up at [rapidapi.com](https://rapidapi.com)
2. **GitHub Repository**: Your code should be in a public GitHub repository
3. **API Documentation**: The API includes comprehensive OpenAPI documentation
4. **Environment Variables**: Set up your API keys and configuration

## API Endpoints

### Base URL
```
https://your-api-domain.rapidapi.com
```

### Authentication
All requests require the `X-RapidAPI-Key` header with your RapidAPI subscription key.

### Available Endpoints

#### 1. Health Check
```http
GET /health
```

#### 2. API Information
```http
GET /
```

#### 3. Experiment Management

**Create Experiment**
```http
POST /api/v1/experiments
Content-Type: application/json
X-RapidAPI-Key: your-api-key

{
  "name": "Email Subject Line Test",
  "description": "Testing different email subject lines for better open rates",
  "variants": [
    {
      "name": "control",
      "template": "Your order has been confirmed",
      "parameters": {},
      "version": "1.0.0"
    },
    {
      "name": "variant_a",
      "template": "🎉 Your order is ready!",
      "parameters": {},
      "version": "1.0.0"
    },
    {
      "name": "variant_b", 
      "template": "Order Confirmed - Thank you for your purchase",
      "parameters": {},
      "version": "1.0.0"
    }
  ],
  "config": {
    "name": "Email Subject Line Test",
    "description": "Testing different email subject lines",
    "traffic_split": {
      "control": 0.33,
      "variant_a": 0.33,
      "variant_b": 0.34
    },
    "min_sample_size": 100,
    "significance_level": 0.05,
    "max_duration_days": 7,
    "early_stopping": true,
    "metrics": ["quality", "cost"],
    "provider": "openai",
    "model": "gpt-3.5-turbo"
  }
}
```

**Start Experiment**
```http
POST /api/v1/experiments/{experiment_id}/start
X-RapidAPI-Key: your-api-key
```

**Stop Experiment**
```http
POST /api/v1/experiments/{experiment_id}/stop
X-RapidAPI-Key: your-api-key
```

**List Experiments**
```http
GET /api/v1/experiments
X-RapidAPI-Key: your-api-key
```

**Get Experiment Details**
```http
GET /api/v1/experiments/{experiment_id}
X-RapidAPI-Key: your-api-key
```

#### 4. Testing

**Test Prompt**
```http
POST /api/v1/test
Content-Type: application/json
X-RapidAPI-Key: your-api-key

{
  "experiment_id": "your-experiment-id",
  "user_id": "user123",
  "input_data": {
    "customer_name": "John Doe",
    "order_number": "ORD-12345",
    "product": "Premium Widget"
  }
}
```

#### 5. Analytics

**Analyze Experiment**
```http
GET /api/v1/experiments/{experiment_id}/analyze
X-RapidAPI-Key: your-api-key
```

**Get Experiment Results**
```http
GET /api/v1/experiments/{experiment_id}/results
X-RapidAPI-Key: your-api-key
```

#### 6. Optimization

**Optimize Prompt**
```http
POST /api/v1/optimize
Content-Type: application/json
X-RapidAPI-Key: your-api-key

{
  "base_prompt": "Write a professional email subject line for order confirmation",
  "optimization_config": {
    "target_metrics": ["quality"],
    "max_iterations": 20,
    "population_size": 10,
    "mutation_rate": 0.1,
    "crossover_rate": 0.8,
    "fitness_threshold": 0.9
  }
}
```

#### 7. Export

**Export Results**
```http
GET /api/v1/experiments/{experiment_id}/export?format=csv
X-RapidAPI-Key: your-api-key
```

#### 8. Configuration

**Get Configuration**
```http
GET /api/v1/config
X-RapidAPI-Key: your-api-key
```

## Response Format

All API responses follow this standard format:

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Deployment Steps

### 1. Prepare Your Code

Ensure your FastAPI application is ready for deployment:

```python
# main.py
from prompt_optimizer.api.server import create_app
from prompt_optimizer.types import OptimizerConfig

# Configure with your API keys
config = OptimizerConfig(
    api_keys={
        "openai": "your-openai-key",
        "anthropic": "your-anthropic-key"
    },
    database_url="postgresql://user:pass@host:port/db"
)

app = create_app(config)
```

### 2. Create Requirements File

```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
llm-prompt-optimizer==0.1.1
python-multipart==0.0.6
```

### 3. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Deploy to RapidAPI

1. **Connect GitHub Repository**:
   - Go to RapidAPI Hub
   - Click "Add New API"
   - Connect your GitHub repository

2. **Configure API Settings**:
   - **API Name**: LLM Prompt Optimizer
   - **Description**: A comprehensive framework for systematic A/B testing and optimization of LLM prompts
   - **Category**: AI & Machine Learning
   - **Base URL**: Your deployed API URL
   - **Authentication**: API Key (X-RapidAPI-Key)

3. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=your-openai-key
   ANTHROPIC_API_KEY=your-anthropic-key
   DATABASE_URL=your-database-url
   ```

4. **Configure Pricing**:
   - **Free Tier**: 100 requests/month
   - **Basic Plan**: $9.99/month - 1,000 requests
   - **Pro Plan**: $29.99/month - 10,000 requests
   - **Enterprise**: Custom pricing

## Usage Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

const options = {
  method: 'POST',
  url: 'https://llm-prompt-optimizer.p.rapidapi.com/api/v1/experiments',
  headers: {
    'content-type': 'application/json',
    'X-RapidAPI-Key': 'your-api-key',
    'X-RapidAPI-Host': 'llm-prompt-optimizer.p.rapidapi.com'
  },
  data: {
    name: 'Email Subject Test',
    variants: [
      {
        name: 'control',
        template: 'Your order confirmation'
      },
      {
        name: 'variant_a',
        template: '🎉 Order confirmed!'
      }
    ],
    config: {
      traffic_split: { control: 0.5, variant_a: 0.5 },
      min_sample_size: 50,
      provider: 'openai',
      model: 'gpt-3.5-turbo'
    }
  }
};

try {
  const response = await axios.request(options);
  console.log(response.data);
} catch (error) {
  console.error(error);
}
```

### Python

```python
import requests

url = "https://llm-prompt-optimizer.p.rapidapi.com/api/v1/experiments"

payload = {
    "name": "Email Subject Test",
    "variants": [
        {
            "name": "control",
            "template": "Your order confirmation"
        },
        {
            "name": "variant_a", 
            "template": "🎉 Order confirmed!"
        }
    ],
    "config": {
        "traffic_split": {"control": 0.5, "variant_a": 0.5},
        "min_sample_size": 50,
        "provider": "openai",
        "model": "gpt-3.5-turbo"
    }
}

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "your-api-key",
    "X-RapidAPI-Host": "llm-prompt-optimizer.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### cURL

```bash
curl --request POST \
  --url https://llm-prompt-optimizer.p.rapidapi.com/api/v1/experiments \
  --header 'content-type: application/json' \
  --header 'X-RapidAPI-Key: your-api-key' \
  --header 'X-RapidAPI-Host: llm-prompt-optimizer.p.rapidapi.com' \
  --data '{
    "name": "Email Subject Test",
    "variants": [
      {
        "name": "control",
        "template": "Your order confirmation"
      },
      {
        "name": "variant_a",
        "template": "🎉 Order confirmed!"
      }
    ],
    "config": {
      "traffic_split": {"control": 0.5, "variant_a": 0.5},
      "min_sample_size": 50,
      "provider": "openai",
      "model": "gpt-3.5-turbo"
    }
  }'
```

## Monitoring and Analytics

### RapidAPI Analytics
- Track API usage and performance
- Monitor error rates and response times
- Analyze user behavior and popular endpoints

### Custom Analytics
- Use the `/api/v1/config` endpoint to monitor system health
- Export experiment results for external analysis
- Track cost and performance metrics

## Support and Documentation

- **API Documentation**: Available at `/docs` endpoint
- **GitHub Repository**: [https://github.com/Sherin-SEF-AI/prompt-optimizer](https://github.com/Sherin-SEF-AI/prompt-optimizer)
- **PyPI Package**: [https://pypi.org/project/llm-prompt-optimizer](https://pypi.org/project/llm-prompt-optimizer)
- **Contact**: sherin.joseph2217@gmail.com

## Best Practices

1. **Rate Limiting**: Implement appropriate rate limits for your use case
2. **Error Handling**: Always check the `success` field in responses
3. **API Keys**: Keep your RapidAPI key secure and rotate regularly
4. **Monitoring**: Set up alerts for high error rates or usage spikes
5. **Documentation**: Keep your API documentation updated

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your X-RapidAPI-Key header
2. **Rate Limit Exceeded**: Check your subscription plan limits
3. **Invalid Request Format**: Ensure JSON payload matches expected schema
4. **Experiment Not Found**: Verify experiment ID exists and is accessible

### Support Channels

- RapidAPI Support: Use the support chat in RapidAPI Hub
- GitHub Issues: Report bugs at the GitHub repository
- Email Support: Contact sherin.joseph2217@gmail.com

---

**Author**: Sherin Joseph Roy  
**Version**: 0.1.1  
**License**: MIT  
**Last Updated**: January 2024 
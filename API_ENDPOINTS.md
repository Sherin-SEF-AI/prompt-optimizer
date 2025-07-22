# LLM Prompt Optimizer API - Complete Endpoint Reference

## Overview

The LLM Prompt Optimizer API provides comprehensive endpoints for A/B testing, optimization, analytics, monitoring, and security features for LLM prompts.

## Base URL
```
http://localhost:8000
```

## Authentication
Set your API keys in the request headers or use the configuration endpoint.

## Response Format
All endpoints return a standardized response format:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 🔍 Health & Information

### Get API Information
```http
GET /
```
Returns API information, documentation links, and available endpoints.

### Health Check
```http
GET /health
```
Returns service health status.

---

## 🧪 Experiment Management

### Create Experiment
```http
POST /api/v1/experiments
```
**Body:**
```json
{
  "name": "My A/B Test",
  "description": "Testing different prompt variants",
  "variants": [
    {
      "name": "variant_a",
      "template": "You are a helpful assistant. {input}",
      "parameters": {}
    },
    {
      "name": "variant_b", 
      "template": "As an AI expert, I can help you with: {input}",
      "parameters": {}
    }
  ],
  "config": {
    "traffic_split": 0.5,
    "min_sample_size": 100,
    "confidence_level": 0.95
  }
}
```

### List Experiments
```http
GET /api/v1/experiments
```
Returns all experiments with their status and metadata.

### Get Experiment Details
```http
GET /api/v1/experiments/{experiment_id}
```
Returns detailed information about a specific experiment.

### Start Experiment
```http
POST /api/v1/experiments/{experiment_id}/start
```
Starts an experiment and begins data collection.

### Stop Experiment
```http
POST /api/v1/experiments/{experiment_id}/stop
```
Stops an experiment and prevents further data collection.

---

## 🧪 Testing & Results

### Test Prompt
```http
POST /api/v1/test
```
**Body:**
```json
{
  "experiment_id": "exp_123",
  "user_id": "user_456",
  "input_data": {
    "question": "What is machine learning?"
  }
}
```

### Get Experiment Results
```http
GET /api/v1/experiments/{experiment_id}/results
```
Returns all test results for an experiment.

### Analyze Experiment
```http
GET /api/v1/experiments/{experiment_id}/analyze
```
Returns comprehensive analysis with statistical significance.

### Export Results
```http
GET /api/v1/experiments/{experiment_id}/export?format=csv
```
Exports results in CSV or JSON format.

---

## 🚀 Optimization

### Optimize Prompt
```http
POST /api/v1/optimize
```
**Body:**
```json
{
  "base_prompt": "You are a helpful assistant.",
  "optimization_config": {
    "max_iterations": 10,
    "population_size": 50,
    "mutation_rate": 0.1
  }
}
```

---

## 📊 Analytics

### Get Cost Summary
```http
GET /api/v1/analytics/cost-summary
```
Returns cost tracking and usage analytics.

### Get Quality Report
```http
GET /api/v1/analytics/quality-report
```
Returns quality scoring and assessment metrics.

### Generate Analytics Report
```http
GET /api/v1/analytics/generate-report?experiment_id=exp_123&report_type=comprehensive
```
Generates comprehensive analytics reports.

### Get Predictive Analytics
```http
GET /api/v1/analytics/predictive?experiment_id=exp_123
```
Returns predictive analytics and forecasting.

---

## 📈 Monitoring

### Get Dashboard Data
```http
GET /api/v1/monitoring/dashboard
```
Returns real-time dashboard metrics and visualizations.

### Get System Metrics
```http
GET /api/v1/monitoring/metrics
```
Returns system performance and health metrics.

---

## 🔒 Security

### Check Content Safety
```http
POST /api/v1/security/check-content
```
**Body:**
```json
{
  "content": "Text to check for safety and compliance"
}
```

### Detect Bias
```http
POST /api/v1/security/detect-bias
```
**Body:**
```json
{
  "text": "Text to check for bias"
}
```

### Check Injection Attacks
```http
POST /api/v1/security/check-injection
```
**Body:**
```json
{
  "prompt": "Prompt to check for injection attacks"
}
```

### Get Audit Logs
```http
GET /api/v1/security/audit-logs?limit=100&offset=0
```
Returns security audit logs with pagination.

### Check Compliance
```http
POST /api/v1/security/compliance-check
```
**Body:**
```json
{
  "experiment_id": "exp_123"
}
```

---

## 🧪 Testing & Statistical Analysis

### Run A/B Test
```http
POST /api/v1/testing/ab-test
```
**Body:**
```json
{
  "experiment_id": "exp_123",
  "sample_size": 100
}
```

### Calculate Statistical Significance
```http
GET /api/v1/testing/significance?experiment_id=exp_123&variant_a=variant_a&variant_b=variant_b
```
Calculates statistical significance between two variants.

---

## ⚙️ Configuration

### Get Configuration
```http
GET /api/v1/config
```
Returns current system configuration and settings.

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

Error responses follow this format:
```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## Rate Limiting

- Free tier: 100 requests/month
- Basic plan: 1,000 requests/month
- Pro plan: 10,000 requests/month
- Enterprise: Custom limits

---

## SDK Examples

### Python
```python
import requests

# Create an experiment
response = requests.post("http://localhost:8000/api/v1/experiments", json={
    "name": "My Test",
    "variants": [...],
    "config": {...}
})

# Test a prompt
response = requests.post("http://localhost:8000/api/v1/test", json={
    "experiment_id": "exp_123",
    "user_id": "user_456",
    "input_data": {...}
})
```

### JavaScript
```javascript
// Create an experiment
const response = await fetch("http://localhost:8000/api/v1/experiments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        name: "My Test",
        variants: [...],
        config: {...}
    })
});

// Test a prompt
const testResponse = await fetch("http://localhost:8000/api/v1/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        experiment_id: "exp_123",
        user_id: "user_456",
        input_data: {...}
    })
});
```

---

## Support

For support and questions:
- Email: sherin.joseph2217@gmail.com
- GitHub: https://github.com/Sherin-SEF-AI/prompt-optimizer.git
- Documentation: `/docs` (Swagger UI)
- Alternative docs: `/redoc` (ReDoc) 
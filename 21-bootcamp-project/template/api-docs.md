# API Documentation

## Base URL

| Environment | URL |
|------------|-----|
| Local | `http://localhost:8000` |
| Staging | `https://[staging-url]` |
| Production | `https://[production-url]` |

## Authentication

All endpoints require an API key in the `Authorization` header.

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://[your-url]/v1/predict
```

| Header | Format | Required |
|--------|--------|----------|
| `Authorization` | `Bearer <api_key>` | Yes |

API keys are generated in the dashboard or via the `/auth/keys` endpoint.

## Rate Limiting

| Tier | Requests/min | Burst |
|------|-------------|-------|
| Free | 10 | 5 |
| Standard | 100 | 20 |
| Enterprise | 1000 | 100 |

Rate limit headers are included in every response:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 97
X-RateLimit-Reset: 1640995200
```

## Endpoints

---

### `GET /health`

Health check endpoint. Returns service status.

**Auth:** None

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400
}
```

---

### `POST /v1/predict`

Main inference endpoint. Accepts input and returns model prediction.

**Auth:** Required

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | string | Yes | Input text or data to process |
| `options` | object | No | Configuration options |

```json
{
  "input": "Your input text here",
  "options": {
    "temperature": 0.7,
    "max_tokens": 512,
    "return_metadata": false
  }
}
```

**Options Schema:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `temperature` | float | 0.7 | Sampling temperature (0.0–2.0) |
| `max_tokens` | int | 256 | Maximum tokens to generate |
| `return_metadata` | bool | false | Include confidence scores, timing |

**Response:** `200 OK`

```json
{
  "id": "req_abc123",
  "result": {
    "prediction": "positive",
    "confidence": 0.94,
    "label": "Positive Sentiment"
  },
  "metadata": {
    "model_version": "v1.2.0",
    "latency_ms": 145,
    "tokens_used": 42
  }
}
```

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| `400` | `INVALID_INPUT` | Input validation failed |
| `401` | `UNAUTHORIZED` | Missing or invalid API key |
| `429` | `RATE_LIMITED` | Too many requests |
| `500` | `INTERNAL_ERROR` | Server error |

---

### `POST /v1/batch`

Batch prediction endpoint for multiple inputs.

**Auth:** Required

**Request Body:**

```json
{
  "inputs": [
    "First input text",
    "Second input text",
    "Third input text"
  ],
  "options": {
    "temperature": 0.7
  }
}
```

**Response:** `200 OK`

```json
{
  "id": "batch_xyz789",
  "results": [
    { "prediction": "positive", "confidence": 0.94 },
    { "prediction": "negative", "confidence": 0.87 },
    { "prediction": "neutral", "confidence": 0.72 }
  ],
  "metadata": {
    "total_items": 3,
    "total_latency_ms": 410
  }
}
```

---

### `GET /v1/metrics`

Returns model performance metrics.

**Auth:** Required

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `window` | string | `24h` | Time window: `1h`, `24h`, `7d`, `30d` |
| `model_version` | string | latest | Filter by model version |

**Response:** `200 OK`

```json
{
  "window": "24h",
  "model_version": "v1.2.0",
  "metrics": {
    "total_requests": 12450,
    "avg_latency_ms": 142,
    "p95_latency_ms": 310,
    "p99_latency_ms": 890,
    "error_rate": 0.002,
    "avg_confidence": 0.88
  }
}
```

---

### `GET /v1/models`

List available models and their versions.

**Auth:** Required

**Response:** `200 OK`

```json
{
  "models": [
    {
      "name": "sentiment-classifier",
      "version": "v1.2.0",
      "status": "active",
      "deployed_at": "2025-01-15T10:30:00Z",
      "metrics": {
        "accuracy": 0.94,
        "f1_score": 0.93
      }
    }
  ]
}
```

## Error Schema

All errors follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {
      "field": "input",
      "reason": "must be a non-empty string"
    }
  }
}
```

| Error Code | HTTP Status | Description |
|------------|------------|-------------|
| `INVALID_INPUT` | 400 | Request body failed validation |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `FORBIDDEN` | 403 | API key lacks required permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `MODEL_ERROR` | 500 | Model inference failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Example Requests

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/predict",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "input": "This product is amazing!",
        "options": {"temperature": 0.3}
    }
)

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "This product is amazing!", "options": {"temperature": 0.3}}'
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/v1/predict', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    input: 'This product is amazing!',
    options: { temperature: 0.3 }
  })
});

const data = await response.json();
console.log(data);
```

## OpenAPI Spec

Auto-generated docs are available at:

| Format | URL |
|--------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| OpenAPI JSON | `http://localhost:8000/openapi.json` |

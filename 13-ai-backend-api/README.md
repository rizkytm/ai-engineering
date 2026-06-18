# Module 13: Developing AI Backend & API Services

## Learning Objectives
By the end of this module, you will be able to:
- Build production-ready AI APIs using FastAPI
- Implement proper request validation with Pydantic
- Integrate LLMs (Google Gemini) into API endpoints
- Handle streaming responses for real-time AI interactions
- Design error handling and retry logic for AI services
- Test and document APIs using Swagger UI and curl

---

## 1. API Concepts in AI Systems

### Request-Response Model
AI services typically follow HTTP request-response patterns:
- **Client** sends request (JSON payload)
- **Server** processes request (may call AI model)
- **Server** returns response (JSON payload)

### REST API Principles
- **Stateless**: Each request contains all needed information
- **Resource-based**: Endpoints represent resources (`/chat`, `/classify`)
- **Standard HTTP methods**: GET (retrieve), POST (create/process), PUT (update), DELETE (remove)

### HTTP Status Codes for AI Services
- `200 OK`: Successful AI inference
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input or parameters
- `401 Unauthorized`: Missing/invalid API key
- `422 Unprocessable Entity`: Validation error (Pydantic)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Model inference failed
- `503 Service Unavailable`: Model loading or service down

### Content Types
- `application/json`: Standard for most AI APIs
- `text/event-stream`: For streaming responses
- `multipart/form-data`: For file uploads (images, audio)

---

## 2. FastAPI Basics

### Why FastAPI for AI?
- **High performance**: Async support, comparable to Node.js/Go
- **Auto-generated docs**: Swagger UI and ReDoc
- **Type safety**: Python type hints for request/response
- **Async support**: Handle concurrent AI requests efficiently
- **WebSocket support**: Real-time AI interactions

### Project Structure
```
ai-backend-api/
├── main.py              # Main application entry
├── routers/             # Route modules
│   ├── chat.py
│   ├── classification.py
├── models/              # Pydantic models
│   ├── requests.py
│   ├── responses.py
├── services/            # Business logic
│   ├── gemini.py
├── dependencies.py      # Dependency injection
└── requirements.txt
```

### Basic FastAPI Application
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Service API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "AI Service API"}

@app.post("/predict")
async def predict(data: InputData):
    # AI inference logic here
    return {"prediction": "result"}
```

---

## 3. AI Service Architecture

### Layered Architecture
```
┌─────────────────┐
│   API Layer     │  ← FastAPI routes, request validation
├─────────────────┤
│   Service Layer │  ← Business logic, AI orchestration
├─────────────────┤
│   Model Layer   │  ← LLM calls, ML inference
├─────────────────┤
│   Data Layer    │  ← Database, cache, file storage
└─────────────────┘
```

### Separation of Concerns
- **Routes**: Handle HTTP request/response, validation
- **Services**: Business logic, AI model orchestration
- **Models**: Data schemas (Pydantic)
- **Dependencies**: Shared resources (DB connections, API clients)

### AI Service Design Patterns
1. **Synchronous**: Client waits for full response
2. **Streaming**: Server sends chunks as generated
3. **Async**: Client polls for results or receives webhook
4. **Queue-based**: Heavy inference queued for batch processing

---

## 4. Pydantic for Request Validation

### BaseModel Usage
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192)
```

### Field Constraints
- `min_length`, `max_length`: String length
- `ge`, `le`, `gt`, `lt`: Numeric bounds
- `pattern`: Regex patterns
- `example`: Documentation examples

### Custom Validators
```python
from pydantic import validator

class APIKeyRequest(BaseModel):
    api_key: str

    @validator('api_key')
    def validate_api_key(cls, v):
        if not v.startswith('sk-'):
            raise ValueError('API key must start with sk-')
        return v
```

---

## 5. Input Validation and Error Handling

### Pydantic Validation Errors
FastAPI automatically returns `422 Unprocessable Entity` for validation errors:
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Custom Error Handling
```python
from fastapi import HTTPException, status

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        response = await openai_service.generate(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI inference failed: {str(e)}"
        )
```

### Global Exception Handler
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal error: {str(exc)}"}
    )
```

---

## 6. Integrating LLM (Gemini) into FastAPI

### Gemini Service Pattern
```python
import google.generativeai as genai
from fastapi import Depends

class OpenAIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = client = openai.OpenAI()')
    
    async def generate(self, prompt: str, **kwargs):
        response = await self.model.generate_content_async(prompt, **kwargs)
        return response.text

# Dependency injection
def get_openai_service():
    return OpenAIService(api_key="YOUR_API_KEY")

@app.post("/chat")
async def chat(
    request: ChatRequest,
    service: OpenAIService = Depends(get_openai_service)
):
    response = await service.generate(request.message)
    return {"response": response}
```

### Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

## 7. Handling Latency, Errors, and Response Formatting

### Timeout Handling
```python
import asyncio
from fastapi import HTTPException

async def call_with_timeout(coro, timeout_seconds=30):
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="AI service timeout"
        )
```

### Retry Logic
```python
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(Exception)
)
async def call_gemini_with_retry(prompt: str):
    return await openai_service.generate(prompt)
```

### Streaming Responses
```python
from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        async for chunk in openai_service.generate_stream(request.message):
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### Response Formatting
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIResponse(BaseModel):
    id: str
    text: str
    model: str
    tokens_used: Optional[int]
    latency_ms: float
    created_at: datetime

@app.post("/chat", response_model=AIResponse)
async def chat(request: ChatRequest):
    start_time = datetime.now()
    
    response = await openai_service.generate(request.message)
    
    latency = (datetime.now() - start_time).total_seconds() * 1000
    
    return AIResponse(
        id=str(uuid.uuid4()),
        text=response,
        model=request.model,
        tokens_used=None,  # Extract from Gemini response
        latency_ms=latency,
        created_at=datetime.now()
    )
```

---

## 8. Testing with Swagger UI and curl

### Swagger UI
FastAPI automatically generates interactive API docs:
- **URL**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Testing with curl
```bash
# Basic chat request
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'

# Streaming response
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a story"}' \
  --no-buffer

# With authentication
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"message": "Hello!"}'
```

### Testing with Python
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Hello, AI!"},
    timeout=30
)

print(response.json())
```

### Load Testing
```bash
# Using hey (install: go install github.com/rakyll/hey@latest)
hey -n 100 -c 10 -m POST \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' \
  http://localhost:8000/chat
```

---

## 9. Production Considerations

### Security
- Validate and sanitize all inputs
- Use API keys or JWT for authentication
- Rate limiting to prevent abuse
- HTTPS in production

### Performance
- Async endpoints for I/O-bound operations
- Connection pooling for external services
- Caching frequent responses
- Background tasks for non-blocking operations

### Monitoring
- Log request/response metadata
- Track latency metrics
- Monitor error rates
- Alert on service degradation

### Deployment
- Docker containerization
- Environment-based configuration
- Health check endpoints
- Graceful shutdown handling

---

## Key Takeaways

1. **FastAPI** is ideal for AI services due to async support and auto-documentation
2. **Pydantic** ensures type safety and validation at the API boundary
3. **Service layer** separates business logic from HTTP concerns
4. **Streaming** provides better UX for long-running AI generation
5. **Error handling** must account for AI service failures and timeouts
6. **Testing** should include both functional and load testing

---

## Next Steps
- Explore Module 14: Deploying AI Services
- Study authentication patterns (OAuth2, JWT)
- Learn containerization with Docker
- Investigate serverless deployment options
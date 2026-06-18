# Exercise 01: Building AI Backend APIs

## Overview
Practice building production-ready AI backend services using FastAPI, Pydantic, and Gemini. Complete each part sequentially.

---

## Part 1: Simple FastAPI App with 3 Endpoints

### Objective
Create a basic FastAPI application with three endpoints.

### Requirements
1. **GET `/`** - Root endpoint returning service info
2. **GET `/models`** - List available AI models
3. **POST `/echo`** - Echo back the input message

### Starter Code
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My AI API")

class EchoRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    # TODO: Return service info
    pass

@app.get("/models")
async def list_models():
    # TODO: Return list of available models
    pass

@app.post("/echo")
async def echo(request: EchoRequest):
    # TODO: Echo back the message
    pass
```

### Validation Checklist
- [ ] Root endpoint returns JSON with service name and version
- [ ] Models endpoint returns list of at least 3 models
- [ ] Echo endpoint accepts and returns a message
- [ ] All endpoints return proper HTTP status codes
- [ ] Run with `uvicorn main:app --reload`
- [ ] Test in browser at `http://localhost:8000/docs`

---

## Part 2: Add Pydantic Validation

### Objective
Enhance the API with comprehensive input validation.

### Requirements
1. **Enhance EchoRequest** with validation:
   - Message must be 1-1000 characters
   - Add optional `uppercase` boolean field (default: false)
   - Add optional `repeat_count` field (1-5, default: 1)

2. **Create new endpoint `/analyze`**:
   - Accept text with minimum length requirement
   - Return analysis results with word count, character count
   - Validate input thoroughly

3. **Add proper error responses**:
   - Return structured error messages
   - Include error type and details

### Starter Code
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import time

app = FastAPI(title="My AI API")

class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    uppercase: bool = Field(default=False)
    repeat_count: int = Field(default=1, ge=1, le=5)

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    include_sentiment: bool = Field(default=False)

class AnalysisResponse(BaseModel):
    word_count: int
    character_count: int
    sentence_count: int
    reading_time_minutes: float

@app.post("/echo")
async def echo(request: EchoRequest):
    # TODO: Implement echo with validation
    pass

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    # TODO: Implement text analysis
    pass
```

### Validation Checklist
- [ ] EchoRequest validates message length (1-1000)
- [ ] repeat_count is constrained to 1-5
- [ ] AnalysisRequest requires minimum 10 characters
- [ ] AnalysisResponse returns all required fields
- [ ] HTTP 422 returned for validation errors
- [ ] Custom error messages are clear

---

## Part 3: Build AI Chat API , with OpenAI

### Objective
Integrate Google OpenAI API for AI-powered chat.

### Requirements
1. **Setup Gemini service**:
   - Create `services/openai_service.py`
   - Implement basic generate method
   - Handle API key from environment

2. **Create `/chat` endpoint**:
   - Accept user message
   - Generate AI response using OpenAI
   - Return response with metadata

3. **Add API key authentication**:
   - Require X-API-Key header
   - Validate against allowed keys

### Starter Code
```python
# services/openai_service.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = client = openai.OpenAI()')
    
    async def generate(self, prompt: str) -> str:
        # TODO: Implement generation
        pass

openai_service = OpenAIService()
```

```python
# main.py
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import time
from datetime import datetime

app = FastAPI()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    id: str
    response: str
    model: str
    latency_ms: float
    created_at: datetime

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    # TODO: Implement API key verification
    pass

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    # TODO: Implement chat , with OpenAI
    pass
```

### Validation Checklist
- [ ] Gemini service initializes with API key
- [ ] Chat endpoint requires valid API key
- [ ] Response includes id, response, model, latency, created_at
- [ ] Error handling for Gemini failures
- [ ] Environment variables properly loaded

---

## Part 4: Add Error Handling and Streaming

### Objective
Implement robust error handling and streaming responses.

### Requirements
1. **Add retry logic**:
   - Implement retry decorator for OpenAI calls
   - Handle transient failures

2. **Create streaming endpoint**:
   - Implement `/chat/stream` with SSE
   - Stream response chunks as they're generated

3. **Add comprehensive error handling**:
   - Custom exception classes
   - Structured error responses
   - Timeout handling

### Starter Code
```python
# utils/retry.py
import asyncio
import functools
from typing import Type, Tuple

def retry_async(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement retry logic
            pass
        return wrapper
    return decorator
```

```python
# main.py additions
from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    async def event_generator():
        try:
            # TODO: Implement streaming
            yield f"data: {json.dumps({'text': 'chunk'})}\\n\\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\\n\\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### Validation Checklist
- [ ] Retry decorator works with exponential backoff
- [ ] Streaming endpoint returns SSE format
- [ ] Error responses include error type and message
- [ ] Timeouts are handled gracefully
- [ ] All exceptions are caught and formatted

---

## Bonus: Build an AI Classification API

### Objective
Create an API that classifies text into categories.

### Requirements
1. **Create `/classify` endpoint**:
   - Accept text and optional category hints
   - Return classification with confidence scores

2. **Implement multiple endpoints**:
   - `/classify/single` - Classify single text
   - `/classify/batch` - Classify multiple texts
   - `/classify/categories` - List available categories

3. **Add advanced validation**:
   - Custom validators for text preprocessing
   - Rate limiting

### Starter Code
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class Category(str, Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    GENERAL = "general"

class ClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    categories: Optional[List[Category]] = None
    
    @validator('text')
    def validate_text(cls, v):
        # TODO: Add text validation
        return v.strip()

class ClassificationResult(BaseModel):
    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: Optional[str] = None

class ClassificationResponse(BaseModel):
    results: List[ClassificationResult]
    processing_time_ms: float
    model: str

@app.post("/classify", response_model=ClassificationResponse)
async def classify(request: ClassificationRequest):
    # TODO: Implement classification
    pass

@app.post("/classify/batch")
async def classify_batch(requests: List[ClassificationRequest]):
    # TODO: Implement batch classification
    pass

@app.get("/classify/categories")
async def list_categories():
    # TODO: Return available categories
    pass
```

### Bonus Requirements
- [ ] Implement batch processing with concurrency control
- [ ] Add caching for repeated classifications
- [ ] Implement rate limiting per API key
- [ ] Add comprehensive logging
- [ ] Create integration tests

---

## Testing Your Implementation

### Manual Testing
```bash
# Start server
uvicorn main:app --reload

# Test endpoints
curl http://localhost:8000/docs  # Open Swagger UI
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"message": "Hello!"}'
```

### Automated Testing
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "Hello!"},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
```

---

## Submission

After completing the exercises:
1. Ensure all endpoints work with Swagger UI
2. Verify error handling returns proper responses
3. Test streaming functionality
4. Document any issues encountered
5. Consider deployment options (Docker, cloud platforms)

---

## Resources
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic Documentation: https://docs.pydantic.dev/
- Google OpenAI API: https://ai.google.dev/
- Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
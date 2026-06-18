from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

from services.openai_service import openai_service
from utils.retry import retry_async

load_dotenv()

app = FastAPI(
    title="AI Chat API",
    description="Production-ready AI chat service with OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Models ====================

class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r"^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=32000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096, description="User message")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    system_instruction: Optional[str] = Field(default=None, max_length=2048)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192)
    stream: bool = Field(default=False, description="Enable streaming response")


class StreamChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    system_instruction: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)


class ChatResponse(BaseModel):
    id: str
    response: str
    model: str
    tokens_used: Optional[int]
    latency_ms: float
    created_at: datetime


class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    request_id: Optional[str]


# ==================== Dependencies ====================

VALID_API_KEYS = os.getenv("API_KEYS", "").split(",")


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header."
        )

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )

    return x_api_key


# ==================== Exception Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status_code": 500
        }
    )


# ==================== Endpoints ====================

@app.get("/")
async def root():
    return {
        "service": "AI Chat API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": "gpt-4o-mini",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/models")
async def list_models():
    return {
        "models": [
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "max_tokens": 16384},
            {"id": "gpt-4o", "name": "GPT-4o", "max_tokens": 16384},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "max_tokens": 128000}
        ]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """Synchronous chat endpoint."""
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Build messages with history
        messages = []

        if request.system_instruction:
            messages.append({"role": "system", "content": request.system_instruction})

        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": request.message})

        # Generate response
        response_text = await openai_service.generate_with_timeout(
            request.message,
            timeout_seconds=30.0,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        latency = (time.time() - start_time) * 1000

        return ChatResponse(
            id=request_id,
            response=response_text,
            model="gpt-4o-mini",
            tokens_used=len(response_text.split()),
            latency_ms=latency,
            created_at=datetime.now()
        )

    except TimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(
    request: StreamChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """Streaming chat endpoint."""
    async def event_generator():
        request_id = str(uuid.uuid4())

        try:
            # Build prompt
            prompt_parts = []

            if request.system_instruction:
                prompt_parts.append(f"System: {request.system_instruction}")

            prompt_parts.append(f"User: {request.message}")
            prompt = "\n".join(prompt_parts)

            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'request_id': request_id})}\n\n"

            # Stream response
            async for chunk in openai_service.agenerate_stream(
                prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'type': 'done', 'request_id': request_id})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/classify")
async def classify_text(
    text: str,
    language: str = "en",
    api_key: str = Depends(verify_api_key)
):
    """Text classification endpoint."""
    try:
        prompt = f"Classify the following text into one of these categories: technical, business, general, other.\n\nText: {text}\n\nReturn only the category name."

        response = await openai_service.generate_with_timeout(
            prompt,
            timeout_seconds=10.0
        )

        return {
            "text": text,
            "category": response.strip().lower(),
            "language": language,
            "model": "gpt-4o-mini"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        )


@app.post("/analyze")
async def analyze_text(
    text: str,
    include_sentiment: bool = False,
    api_key: str = Depends(verify_api_key)
):
    """Text analysis endpoint."""
    try:
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        reading_time = word_count / 200  # Average reading speed: 200 wpm

        result = {
            "word_count": word_count,
            "character_count": char_count,
            "sentence_count": sentence_count,
            "reading_time_minutes": round(reading_time, 2)
        }

        if include_sentiment:
            sentiment_prompt = f"Determine the sentiment of this text as positive, negative, or neutral:\n\nText: {text}\n\nReturn only the sentiment."
            sentiment = await openai_service.generate_with_timeout(
                sentiment_prompt,
                timeout_seconds=10.0
            )
            result["sentiment"] = sentiment.strip().lower()

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

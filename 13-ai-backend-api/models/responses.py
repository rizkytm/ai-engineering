from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ChatResponse(BaseModel):
    """Response model for chat completion."""
    id: str = Field(..., description="Unique response ID")
    response: str = Field(..., description="AI response text")
    model: str = Field(..., description="Model used for generation")
    tokens_used: Optional[int] = Field(default=None, description="Number of tokens used")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    created_at: datetime = Field(default_factory=datetime.now, description="Response creation timestamp")


class UsageInfo(BaseModel):
    """Token usage information."""
    prompt_tokens: int = Field(ge=0, description="Number of prompt tokens")
    completion_tokens: int = Field(ge=0, description="Number of completion tokens")
    total_tokens: int = Field(ge=0, description="Total number of tokens")


class Choice(BaseModel):
    """A single choice in a completion response."""
    index: int = Field(ge=0, description="Choice index")
    message: Dict[str, Any] = Field(..., description="Message content")
    finish_reason: str = Field(..., description="Reason for finishing")


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response."""
    id: str = Field(..., description="Unique response ID")
    object: str = Field(default="chat.completion", description="Object type")
    created: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    model: str = Field(..., description="Model used")
    choices: List[Choice] = Field(..., description="Response choices")
    usage: UsageInfo = Field(..., description="Token usage information")


class ClassificationResult(BaseModel):
    """A single classification result."""
    label: str = Field(..., description="Classification label")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    reasoning: Optional[str] = Field(default=None, description="Reasoning for classification")


class ClassificationResponse(BaseModel):
    """Response model for text classification."""
    results: List[ClassificationResult] = Field(..., description="Classification results")
    model: str = Field(..., description="Model used for classification")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class GenerationResponse(BaseModel):
    """Response model for text generation."""
    id: str = Field(..., description="Unique response ID")
    text: str = Field(..., description="Generated text")
    model: str = Field(..., description="Model used")
    tokens_used: Optional[int] = Field(default=None, description="Number of tokens used")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    created_at: datetime = Field(default_factory=datetime.now, description="Response creation timestamp")


class ErrorDetail(BaseModel):
    """Detailed error information."""
    loc: List[str] = Field(..., description="Error location")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(default=None, description="Detailed errors")
    status_code: int = Field(..., description="HTTP status code")
    request_id: Optional[str] = Field(default=None, description="Request ID for debugging")
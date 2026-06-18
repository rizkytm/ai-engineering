from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """A message in a conversation."""
    role: MessageRole = Field(..., description="Role of the message sender")
    content: str = Field(..., min_length=1, max_length=32000, description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    message: str = Field(..., min_length=1, max_length=4096, description="User message")
    history: List[Message] = Field(default_factory=list, description="Conversation history")
    system_instruction: Optional[str] = Field(default=None, max_length=2048, description="System instruction")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192, description="Maximum tokens to generate")
    stream: bool = Field(default=False, description="Enable streaming response")


class StreamChatRequest(BaseModel):
    """Request model for streaming chat completion."""
    message: str = Field(..., min_length=1, max_length=4096, description="User message")
    system_instruction: Optional[str] = Field(default=None, max_length=2048, description="System instruction")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192, description="Maximum tokens to generate")


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class TextClassificationRequest(BaseModel):
    """Request model for text classification."""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to classify")
    language: str = Field(default="en", pattern=r"^[a-z]{2}$", description="Language code")
    return_confidence: bool = Field(default=True, description="Whether to return confidence scores")


class GenerationMode(str, Enum):
    STANDARD = "standard"
    STREAMING = "streaming"
    BATCH = "batch"


class GenerationRequest(BaseModel):
    """Request model for text generation."""
    mode: GenerationMode = Field(..., description="Generation mode")
    prompt: str = Field(..., min_length=1, max_length=10000, description="Input prompt")
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192, description="Maximum tokens")
    batch_size: Optional[int] = Field(default=None, ge=1, le=100, description="Batch size for batch mode")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature")
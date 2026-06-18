# Services

This directory contains service classes for external API integrations.

## Gemini Service

The `OpenAIService` class provides a wrapper around the Google OpenAI API with:

- **Basic generation**: `generate(prompt, **kwargs)`
- **Streaming generation**: `generate_stream(prompt, **kwargs)`
- **Timeout handling**: `generate_with_timeout(prompt, timeout_seconds, **kwargs)`

### Usage

```python
from services.openai_service import openai_service

# Basic generation
response = await openai_service.generate("Explain quantum computing")

# Streaming
async for chunk in openai_service.generate_stream("Tell me a story"):
    print(chunk, end="")

# With timeout
response = await openai_service.generate_with_timeout(
    "Hello",
    timeout_seconds=10.0
)
```

### Configuration

Set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-api-key
```
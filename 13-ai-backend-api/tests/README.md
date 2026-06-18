# Tests

This directory contains test files for the AI Backend API.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run with coverage
pytest --cov=.
```

## Test Files

- `test_main.py`: Tests for main FastAPI endpoints
- `test_gemini.py`: Tests for Gemini service
- `conftest.py`: Pytest fixtures and configuration

## Test Coverage

Tests cover:
- Endpoint functionality
- Input validation
- API key authentication
- Error handling
- Service integration (mocked)

## Writing Tests

### Example Test

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_example_endpoint():
    response = client.get("/example")
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

### Async Tests

```python
import pytest
from services.openai_service import openai_service

@pytest.mark.asyncio
async def test_async_operation():
    result = await openai_service.generate("test")
    assert isinstance(result, str)
```
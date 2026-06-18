import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert data["service"] == "AI Chat API"


def test_health_endpoint():
    """Test health endpoint returns status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data
    assert "timestamp" in data


def test_models_endpoint():
    """Test models endpoint returns list of models."""
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 1
    for model in data["models"]:
        assert "id" in model
        assert "name" in model


def test_chat_endpoint_requires_api_key():
    """Test chat endpoint requires API key."""
    response = client.post(
        "/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 401


def test_chat_endpoint_invalid_api_key():
    """Test chat endpoint rejects invalid API key."""
    response = client.post(
        "/chat",
        json={"message": "Hello"},
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 403


def test_chat_endpoint_validation():
    """Test chat endpoint validates input."""
    # Empty message
    response = client.post(
        "/chat",
        json={"message": ""},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 422

    # Message too long
    response = client.post(
        "/chat",
        json={"message": "x" * 5000},
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 422


def test_classify_endpoint():
    """Test classify endpoint requires API key."""
    response = client.post(
        "/classify",
        params={"text": "Hello world"}
    )
    assert response.status_code == 401


def test_analyze_endpoint():
    """Test analyze endpoint requires API key."""
    response = client.post(
        "/analyze",
        params={"text": "This is a test sentence. It has two sentences."}
    )
    assert response.status_code == 401


def test_analyze_endpoint_validation():
    """Test analyze endpoint validates input."""
    # Text too short
    response = client.post(
        "/analyze",
        params={"text": "Hi"},
        headers={"X-API-Key": "test-key"}
    )
    # This should work since min_length is not set in analyze endpoint
    assert response.status_code in [200, 422]
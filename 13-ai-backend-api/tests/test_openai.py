import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from services.openai_service import OpenAIService


@pytest.fixture
def mock_openai_service():
    """Create a mock OpenAI service for testing."""
    with patch('services.openai_service.openai') as mock_openai:
        # Mock the client
        mock_client = MagicMock()
        mock_async_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        mock_openai.AsyncOpenAI.return_value = mock_async_client
        
        # Create service instance
        service = OpenAIService()
        
        # Mock chat completions
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_async_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        yield service, mock_client, mock_async_client


@pytest.mark.asyncio
async def test_openai_service_generate(mock_openai_service):
    """Test OpenAI service generate method."""
    service, mock_client, _ = mock_openai_service
    
    result = await service.agenerate("Test prompt")
    
    assert result == "Test response"
    mock_async_client = mock_openai_service[2]
    mock_async_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_openai_service_generate_with_timeout(mock_openai_service):
    """Test OpenAI service generate with timeout."""
    service, _, _ = mock_openai_service
    
    result = await service.generate_with_timeout(
        "Test prompt",
        timeout_seconds=5.0
    )
    
    assert result == "Test response"


def test_openai_service_initialization():
    """Test OpenAI service initialization."""
    with patch('services.openai_service.openai') as mock_openai:
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            service = OpenAIService()
            
            mock_openai.OpenAI.assert_called_once_with(api_key='test-key')
            assert service.model == "gpt-4o-mini"


def test_openai_service_initialization_without_key():
    """Test OpenAI service initialization without API key."""
    with patch('services.openai_service.openai') as mock_openai:
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                OpenAIService()

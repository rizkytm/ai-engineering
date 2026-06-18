import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-openai-key',
        'API_KEYS': 'test-key-1,test-key-2'
    }):
        yield


@pytest.fixture
def test_api_key():
    """Return a test API key."""
    return "test-key-1"


@pytest.fixture
def invalid_api_key():
    """Return an invalid API key."""
    return "invalid-key"

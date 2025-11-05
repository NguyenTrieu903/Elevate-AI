"""Test package for RAG chatbot system."""

import sys
from pathlib import Path

# Add project root to path for all test modules
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Test configuration
import pytest

# Configure pytest with default options
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "slow: marks tests as slow running")

# Test fixtures available to all test modules
@pytest.fixture(scope="session")
def project_root_path():
    """Provide project root path to tests."""
    return Path(__file__).parent.parent

@pytest.fixture
def sample_env_vars(monkeypatch):
    """Provide sample environment variables for testing."""
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")
    monkeypatch.setenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
    monkeypatch.setenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

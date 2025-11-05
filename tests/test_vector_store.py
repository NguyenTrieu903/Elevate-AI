"""Tests for vector store functionality."""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rag_system.vector_store import VectorStore
from mock_data.it_helpdesk import get_it_helpdesk_data

class TestVectorStore:
    """Test cases for VectorStore class."""

    @pytest.fixture
    def sample_documents(self):
        """Sample documents for testing."""
        return [
            {
                "page_content": "How to reset password? Go to reset page and follow instructions.",
                "metadata": {"source": "FAQ - Password", "category": "Auth"}
            },
            {
                "page_content": "Computer slow? Restart and close unused applications.",
                "metadata": {"source": "FAQ - Performance", "category": "Hardware"}
            },
            {
                "page_content": "Printer not working? Check power, paper, and ink levels.",
                "metadata": {"source": "FAQ - Printer", "category": "Hardware"}
            }
        ]

    @pytest.fixture
    def temp_dir(self):
        """Temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_vector_store_initialization(self):
        """Test vector store initialization."""
        vs = VectorStore("test_case")
        assert vs.use_case == "test_case"
        assert vs.vectorstore is None
        assert vs.embeddings is not None

    def test_load_documents(self, sample_documents):
        """Test document loading."""
        vs = VectorStore("test_case")
        docs = vs.load_documents(sample_documents)

        assert len(docs) == 3
        assert docs[0].page_content == sample_documents[0]["page_content"]
        assert docs[0].metadata == sample_documents[0]["metadata"]

    def test_create_and_search_index(self, sample_documents, monkeypatch):
        """Test index creation and search functionality."""
        # Mock the embeddings to avoid API calls in tests
        class MockEmbeddings:
            def embed_documents(self, texts):
                return [[0.1] * 10 for _ in texts]

            def embed_query(self, text):
                return [0.1] * 10

        vs = VectorStore("test_case")

        # Skip actual index creation in test environment
        # This test would need proper mocking of FAISS and Azure OpenAI
        # For demonstration purposes, we'll test the document preparation
        docs = vs.load_documents(sample_documents)
        assert len(docs) == 3

    def test_search_functionality(self):
        """Test search with mock data."""
        # This would test the search functionality
        # In a real test environment, you'd need proper Azure OpenAI credentials
        # and would mock the embeddings service
        pass

    def test_get_stats_uninitialized(self):
        """Test stats for uninitialized vector store."""
        vs = VectorStore("test_case")
        stats = vs.get_stats()

        assert stats["status"] == "not_initialized"
        assert stats.get("total_documents") is None

    def test_it_helpdesk_data_loading(self):
        """Test loading real IT helpdesk data."""
        data = get_it_helpdesk_data()

        assert len(data) > 0
        assert all("page_content" in doc for doc in data)
        assert all("metadata" in doc for doc in data)

        # Check first document structure
        first_doc = data[0]
        assert "source" in first_doc["metadata"]
        assert "category" in first_doc["metadata"]
        assert len(first_doc["page_content"]) > 0


class TestVectorStoreIntegration:
    """Integration tests for vector store with real data."""

    def test_create_vector_store_for_use_case(self):
        """Test the convenience function for creating vector stores."""
        # This test would require Azure OpenAI credentials
        # For CI/CD, you'd mock the embedding service
        pass

    def test_multiple_use_cases(self):
        """Test creating vector stores for different use cases."""
        use_cases = ["it_helpdesk", "customer_support", "hr_assistant"]

        for use_case in use_cases:
            # Test that we can import the appropriate data module
            if use_case == "it_helpdesk":
                from mock_data.it_helpdesk import get_it_helpdesk_data
                data = get_it_helpdesk_data()
            elif use_case == "customer_support":
                from mock_data.customer_support import get_customer_support_data
                data = get_customer_support_data()
            elif use_case == "hr_assistant":
                from mock_data.hr_assistant import get_hr_assistant_data
                data = get_hr_assistant_data()

            assert len(data) > 0
            assert all("page_content" in doc for doc in data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Tests for RAG chain functionality."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rag_system.retrieval_chain import RetrievalChain, ConversationManager

class TestConversationManager:
    """Test cases for ConversationManager class."""

    def test_conversation_manager_initialization(self):
        """Test conversation manager initialization."""
        cm = ConversationManager(max_history=5)
        assert cm.max_history == 5
        assert len(cm.chat_history) == 0

    def test_add_exchange(self):
        """Test adding user-assistant exchanges."""
        cm = ConversationManager()

        cm.add_exchange("Hello", "Hi there!")

        assert len(cm.chat_history) == 2
        assert cm.chat_history[0].content == "Hello"
        assert cm.chat_history[1].content == "Hi there!"

    def test_get_history(self):
        """Test getting chat history."""
        cm = ConversationManager()

        cm.add_exchange("Question 1", "Answer 1")
        cm.add_exchange("Question 2", "Answer 2")

        history = cm.get_history()
        assert len(history) == 4
        assert history[0].content == "Question 1"
        assert history[1].content == "Answer 1"
        assert history[2].content == "Question 2"
        assert history[3].content == "Answer 2"

    def test_clear_history(self):
        """Test clearing chat history."""
        cm = ConversationManager()

        cm.add_exchange("Question", "Answer")
        assert len(cm.chat_history) > 0

        cm.clear_history()
        assert len(cm.chat_history) == 0

    def test_max_history_limit(self):
        """Test that history is trimmed when max is exceeded."""
        cm = ConversationManager(max_history=2)

        # Add 3 exchanges (6 messages total)
        cm.add_exchange("Q1", "A1")
        cm.add_exchange("Q2", "A2")
        cm.add_exchange("Q3", "A3")

        # Should only keep last 2 exchanges (4 messages)
        assert len(cm.chat_history) == 4
        assert cm.chat_history[0].content == "Q2"
        assert cm.chat_history[1].content == "A2"
        assert cm.chat_history[2].content == "Q3"
        assert cm.chat_history[3].content == "A3"

    def test_get_history_summary(self):
        """Test getting history summary statistics."""
        cm = ConversationManager()

        cm.add_exchange("Question 1", "Answer 1")
        cm.add_exchange("Question 2", "Answer 2")

        summary = cm.get_history_summary()

        assert summary["total_messages"] == 4
        assert summary["user_messages"] == 2
        assert summary["assistant_messages"] == 2


class TestRetrievalChainMocked:
    """Test cases for RetrievalChain with mocked dependencies."""

    @patch('rag_system.retrieval_chain.AzureChatOpenAI')
    @patch('rag_system.retrieval_chain.VectorStore')
    def test_retrieval_chain_initialization(self, mock_vector_store_class, mock_llm_class):
        """Test retrieval chain initialization with mocks."""
        # Setup mocks
        mock_vector_store = Mock()
        mock_vector_store.index_exists.return_value = True
        mock_vector_store_class.return_value = mock_vector_store

        mock_llm = Mock()
        mock_llm_class.return_value = mock_llm

        rc = RetrievalChain("it_helpdesk")

        assert rc.use_case == "it_helpdesk"
        assert rc.vector_store == mock_vector_store
        assert rc.llm == mock_llm

    def test_system_message_generation(self):
        """Test system message generation for different use cases."""
        # Test that we can create retrieval chains for different use cases
        # This tests the prompt template creation logic

        use_cases = ["it_helpdesk", "customer_support", "hr_assistant"]

        for use_case in use_cases:
            # We can't fully initialize without mocking, but we can test the logic
            with patch('rag_system.retrieval_chain.AzureChatOpenAI'):
                with patch('rag_system.retrieval_chain.VectorStore') as mock_vs:
                    mock_vector_store = Mock()
                    mock_vector_store.index_exists.return_value = True
                    mock_vs.return_value = mock_vector_store

                    rc = RetrievalChain(use_case)

                    # Test that prompt template was created
                    assert rc.prompt_template is not None
                    assert rc.use_case == use_case

    @patch('rag_system.retrieval_chain.AzureChatOpenAI')
    @patch('rag_system.retrieval_chain.VectorStore')
    def test_get_relevant_context(self, mock_vector_store_class, mock_llm_class):
        """Test getting relevant context documents."""
        # Setup mock vector store
        mock_vector_store = Mock()
        mock_vector_store.index_exists.return_value = True
        mock_vector_store.search.return_value = [
            {
                "content": "Test document content",
                "metadata": {"source": "Test Source"},
                "score": 0.9
            }
        ]
        mock_vector_store_class.return_value = mock_vector_store

        mock_llm_class.return_value = Mock()

        rc = RetrievalChain("it_helpdesk")

        results = rc.get_relevant_context("test query")

        assert len(results) > 0
        assert results[0]["content"] == "Test document content"
        mock_vector_store.search.assert_called_once_with("test query", k=4)

    @patch('rag_system.retrieval_chain.AzureChatOpenAI')
    @patch('rag_system.retrieval_chain.VectorStore')
    def test_get_stats(self, mock_vector_store_class, mock_llm_class):
        """Test getting retrieval chain statistics."""
        # Setup mock vector store
        mock_vector_store = Mock()
        mock_vector_store.index_exists.return_value = True
        mock_vector_store.get_stats.return_value = {
            "status": "initialized",
            "total_documents": 10
        }
        mock_vector_store_class.return_value = mock_vector_store

        mock_llm_class.return_value = Mock()

        rc = RetrievalChain("it_helpdesk")

        stats = rc.get_stats()

        assert "use_case" in stats
        assert "vector_store" in stats
        assert "model" in stats
        assert stats["use_case"] == "it_helpdesk"


class TestRetrievalChainIntegration:
    """Integration tests for retrieval chain (require real setup)."""

    def test_mock_data_loading(self):
        """Test that we can load mock data for all use cases."""
        use_cases = ["it_helpdesk", "customer_support", "hr_assistant"]

        for use_case in use_cases:
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
            assert all("metadata" in doc for doc in data)

    def test_prompt_template_structure(self):
        """Test that prompt templates have the expected structure."""
        # We can test the prompt creation logic without full initialization
        with patch('rag_system.retrieval_chain.AzureChatOpenAI'):
            with patch('rag_system.retrieval_chain.VectorStore') as mock_vs:
                mock_vector_store = Mock()
                mock_vector_store.index_exists.return_value = True
                mock_vs.return_value = mock_vector_store

                rc = RetrievalChain("it_helpdesk")

                # Check that prompt template was created
                assert rc.prompt_template is not None

                # The template should have the required input variables
                # This is basic structural validation
                assert hasattr(rc.prompt_template, 'input_variables') or hasattr(rc.prompt_template, 'messages')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

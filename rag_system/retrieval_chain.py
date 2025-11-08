"""Retrieval chain implementation using Langchain for RAG workflow."""

import os
from typing import List, Dict, Any, Optional, Tuple

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from .vector_store import VectorStore

# Load environment variables
load_dotenv()

class RetrievalChain:
    """RAG chain for document retrieval and generation."""

    def __init__(self, use_case: str = "it_helpdesk"):
        """Initialize retrieval chain with specified use case.

        Args:
            use_case: The use case for the retrieval chain
        """
        self.use_case = use_case
        self.vector_store = VectorStore(use_case)
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        self.chain = self._create_chain()

        # Load or create vector index
        self._initialize_vector_store()

    def _initialize_llm(self) -> AzureChatOpenAI:
        """Initialize Azure Chat OpenAI model."""
        # Use LLM-specific credentials if available, otherwise fallback to general ones
        llm_endpoint = os.getenv("AZURE_OPENAI_LLM_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
        llm_key = os.getenv("AZURE_OPENAI_LLM_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        llm_deployment = os.getenv("AZURE_OPENAI_LLM_MODEL") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "GPT-4o-mini")
        llm_api_version = os.getenv("AZURE_OPENAI_LLM_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        return AzureChatOpenAI(
            azure_deployment=llm_deployment,
            azure_endpoint=llm_endpoint,
            api_key=llm_key,
            api_version=llm_api_version,
            temperature=0.7
        )

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create prompt template based on use case."""
        system_message = """You are an experienced IT helpdesk assistant. Help users solve technical problems by:
1. Using the provided knowledge base context to give accurate solutions when available
2. Providing step-by-step troubleshooting instructions
3. Using your general IT knowledge to help when context doesn't have specific information
4. Being concise but thorough in your explanations

Context from knowledge base:
{context}

IMPORTANT: 
- If the context above contains relevant information, use it to provide accurate answers
- If the context is empty or doesn't have specific information, use your general IT knowledge to provide helpful guidance
- Always try to be helpful and provide useful information based on your knowledge
- Only suggest contacting IT support if the issue is truly complex or requires system-level access"""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

    def _create_chain(self):
        """Create the RAG chain."""
        def format_docs(docs):
            """Format retrieved documents for context."""
            if not docs:
                return ""  # Return empty string instead of message, let LLM use its knowledge

            formatted = []
            for i, doc in enumerate(docs, 1):
                content = doc['content']
                metadata = doc['metadata']
                source = metadata.get('source', 'Unknown source')
                category = metadata.get('category', 'General')
                score = doc.get('score', 0)
                
                # Include relevance score for transparency
                formatted.append(f"Document {i} ({category} - {source}, relevance: {score:.2f}):\n{content}")

            return "\n\n".join(formatted)

        def retrieve_docs(input_dict):
            """Retrieve relevant documents."""
            question = input_dict["question"]
            # Use same threshold as in chat() method
            docs = self.vector_store.search(question, k=4, score_threshold=0.5)
            return format_docs(docs)

        # Create the chain
        from operator import itemgetter
        
        chain = (
            {
                "context": retrieve_docs,
                "question": itemgetter("question"),
                "chat_history": itemgetter("chat_history")
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

        return chain

    def _initialize_vector_store(self):
        """Initialize vector store with appropriate data."""
        if not self.vector_store.index_exists():
            print(f"Creating vector index for {self.use_case}...")

            # Import appropriate data based on use case
            if self.use_case == "it_helpdesk":
                from mock_data.it_helpdesk import get_it_helpdesk_data
                documents = get_it_helpdesk_data()
            else:
                raise ValueError(f"Unknown use case: {self.use_case}")

            self.vector_store.create_index(documents)
        else:
            print(f"Loading existing vector index for {self.use_case}...")
            self.vector_store.load_index()

    def chat(
        self,
        question: str,
        chat_history: Optional[List[BaseMessage]] = None
    ) -> Dict[str, Any]:
        """Process a chat message with RAG.

        Args:
            question: User question
            chat_history: Previous chat messages

        Returns:
            Response with answer and retrieved documents
        """
        if chat_history is None:
            chat_history = []

        try:
            # Retrieve relevant documents with minimum relevance threshold
            retrieved_docs = self.vector_store.search(question, k=4, score_threshold=0.5)
            
            # If no relevant documents found (similarity < 0.5), use LLM directly without context
            if not retrieved_docs:
                print(f"ℹ️ No relevant documents found (similarity < 0.5) for query: {question}")
                print(f"   Using LLM directly without knowledge base context.")
                
                # Create a simple prompt without RAG context
                direct_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an experienced IT helpdesk assistant. Help users with technical problems using your knowledge. Provide helpful, accurate information and step-by-step guidance. Be proactive and helpful in your responses."),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}")
                ])
                
                # Generate response directly from LLM without context
                direct_chain = direct_prompt | self.llm | StrOutputParser()
                response = direct_chain.invoke({
                    "question": question,
                    "chat_history": chat_history
                })
                
                return {
                    "answer": response,
                    "retrieved_documents": [],
                    "sources": [],
                    "method": "llm_direct"  # Indicate this is direct LLM call
                }
            
            # Generate response using RAG chain with context
            response = self.chain.invoke({
                "question": question,
                "chat_history": chat_history
            })

            return {
                "answer": response,
                "retrieved_documents": retrieved_docs,
                "sources": [doc['metadata'].get('source', 'Unknown') for doc in retrieved_docs],
                "method": "rag_retrieval"  # Indicate this is RAG with context
            }

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ Error in RAG retrieval: {str(e)}")
            print(f"   Traceback: {error_trace}")
            return {
                "answer": f"I apologize, but I encountered an error processing your request: {str(e)}",
                "retrieved_documents": [],
                "sources": [],
                "error": str(e)
            }

    def get_relevant_context(self, question: str, k: int = 4) -> List[Dict[str, Any]]:
        """Get relevant context documents for a question.

        Args:
            question: User question
            k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        return self.vector_store.search(question, k=k)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add new documents to the knowledge base.

        Args:
            documents: List of documents to add
        """
        self.vector_store.add_documents(documents)

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the retrieval chain."""
        vector_stats = self.vector_store.get_stats()
        model = os.getenv("AZURE_OPENAI_LLM_MODEL") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "GPT-4o-mini")
        return {
            "use_case": self.use_case,
            "vector_store": vector_stats,
            "model": model
        }


class ConversationManager:
    """Manages conversation history and context."""

    def __init__(self, max_history: int = 10):
        """Initialize conversation manager.

        Args:
            max_history: Maximum number of message pairs to keep
        """
        self.max_history = max_history
        self.chat_history: List[BaseMessage] = []

    def add_exchange(self, user_message: str, assistant_message: str):
        """Add a user-assistant message exchange.

        Args:
            user_message: User's message
            assistant_message: Assistant's response
        """
        self.chat_history.extend([
            HumanMessage(content=user_message),
            AIMessage(content=assistant_message)
        ])

        # Trim history if it exceeds max length
        if len(self.chat_history) > self.max_history * 2:
            self.chat_history = self.chat_history[-self.max_history * 2:]

    def get_history(self) -> List[BaseMessage]:
        """Get current chat history."""
        return self.chat_history.copy()

    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []

    def get_history_summary(self) -> Dict[str, Any]:
        """Get a summary of chat history."""
        return {
            "total_messages": len(self.chat_history),
            "user_messages": len([msg for msg in self.chat_history if isinstance(msg, HumanMessage)]),
            "assistant_messages": len([msg for msg in self.chat_history if isinstance(msg, AIMessage)])
        }


if __name__ == "__main__":
    # Test the retrieval chain
    print("Testing Retrieval Chain...")

    # Test IT helpdesk chain
    chain = RetrievalChain("it_helpdesk")

    # Test conversation
    conv_manager = ConversationManager()

    # Test questions
    test_questions = [
        "My computer is running very slowly, what should I do?",
        "How do I reset my password?",
        "The printer is not working, can you help?"
    ]

    for question in test_questions:
        print(f"\nQ: {question}")

        result = chain.chat(question, conv_manager.get_history())
        print(f"A: {result['answer']}")

        if result['retrieved_documents']:
            print(f"Sources: {', '.join(result['sources'])}")

        # Add to conversation history
        conv_manager.add_exchange(question, result['answer'])

    # Print chain stats
    stats = chain.get_stats()
    print(f"\nChain Stats: {stats}")

    # Print conversation summary
    conv_summary = conv_manager.get_history_summary()
    print(f"Conversation Summary: {conv_summary}")

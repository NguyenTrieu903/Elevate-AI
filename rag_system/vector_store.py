"""Vector store implementation using FAISS for fast similarity search."""

import os
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path

import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorStore:
    """FAISS-based vector store for document retrieval."""

    def __init__(self, use_case: str = "it_helpdesk"):
        """Initialize vector store with specified use case.

        Args:
            use_case: The use case for the vector store (it_helpdesk, customer_support, hr_assistant)
        """
        self.use_case = use_case
        self.embeddings = self._initialize_embeddings()
        self.vectorstore: Optional[FAISS] = None
        self.index_path = f"./vector_indexes/{use_case}_index"

        # Create vector indexes directory if it doesn't exist
        Path("./vector_indexes").mkdir(exist_ok=True)

    def _initialize_embeddings(self) -> AzureOpenAIEmbeddings:
        """Initialize Azure OpenAI embeddings."""
        # Use Embedding-specific credentials if available, otherwise fallback to general ones
        embedding_endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
        embedding_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        embedding_deployment = os.getenv("AZURE_OPENAI_EMBED_MODEL") or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
        embedding_api_version = os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        return AzureOpenAIEmbeddings(
            azure_deployment=embedding_deployment,
            model=embedding_deployment,
            azure_endpoint=embedding_endpoint,
            api_key=embedding_key,
            api_version=embedding_api_version
        )

    def load_documents(self, documents: List[Dict[str, Any]]) -> List[Document]:
        """Convert document dictionaries to Langchain Document objects.

        Args:
            documents: List of document dictionaries with 'page_content' and 'metadata'

        Returns:
            List of Langchain Document objects
        """
        return [
            Document(
                page_content=doc["page_content"],
                metadata=doc["metadata"]
            )
            for doc in documents
        ]

    def create_index(self, documents: List[Dict[str, Any]], force_recreate: bool = False) -> None:
        """Create FAISS index from documents.

        Args:
            documents: List of document dictionaries
            force_recreate: Whether to force recreation of existing index
        """
        if not force_recreate and self.index_exists():
            print(f"Loading existing index for {self.use_case}...")
            self.load_index()
            return

        print(f"Creating new FAISS index for {self.use_case}...")

        # Convert to Langchain Documents
        docs = self.load_documents(documents)

        if not docs:
            raise ValueError("No documents provided for indexing")

        # Create FAISS index
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

        # Save the index
        self.save_index()
        print(f"Index created and saved with {len(docs)} documents")

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add new documents to existing index.

        Args:
            documents: List of document dictionaries to add
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Create index first.")

        docs = self.load_documents(documents)
        self.vectorstore.add_documents(docs)
        self.save_index()
        print(f"Added {len(docs)} documents to existing index")

    def search(self, query: str, k: int = 4, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar documents.

        Args:
            query: Search query
            k: Number of documents to return
            score_threshold: Minimum similarity score threshold

        Returns:
            List of similar documents with scores
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Load or create index first.")

        # Perform similarity search with scores
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        # Filter by score threshold and format results
        filtered_results = []
        for doc, score in results:
            # FAISS returns distance (lower is better), convert to similarity
            similarity = 1 / (1 + score)

            if similarity >= score_threshold:
                filtered_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": similarity
                })

        return filtered_results

    def save_index(self) -> None:
        """Save FAISS index to disk."""
        if self.vectorstore is None:
            raise ValueError("No vector store to save")

        # Save FAISS index
        self.vectorstore.save_local(self.index_path)
        print(f"Index saved to {self.index_path}")

    def load_index(self) -> None:
        """Load FAISS index from disk."""
        if not self.index_exists():
            raise FileNotFoundError(f"Index not found at {self.index_path}")

        # Load FAISS index
        self.vectorstore = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Index loaded from {self.index_path}")

    def index_exists(self) -> bool:
        """Check if index exists on disk."""
        return Path(f"{self.index_path}.faiss").exists()

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        if self.vectorstore is None:
            return {"status": "not_initialized"}

        return {
            "status": "initialized",
            "total_documents": self.vectorstore.index.ntotal,
            "embedding_dimension": self.vectorstore.index.d,
            "use_case": self.use_case
        }

    def delete_index(self) -> None:
        """Delete the index files."""
        index_files = [
            f"{self.index_path}.faiss",
            f"{self.index_path}.pkl"
        ]

        for file_path in index_files:
            if Path(file_path).exists():
                Path(file_path).unlink()
                print(f"Deleted {file_path}")

        self.vectorstore = None
        print("Index deleted successfully")


def create_vector_store_for_use_case(use_case: str, force_recreate: bool = False) -> VectorStore:
    """Create vector store for a specific use case.

    Args:
        use_case: The use case (it_helpdesk, customer_support, hr_assistant)
        force_recreate: Whether to force recreation of existing index

    Returns:
        Initialized VectorStore instance
    """
    # Import the appropriate data module
    if use_case == "it_helpdesk":
        from mock_data.it_helpdesk import get_it_helpdesk_data
        documents = get_it_helpdesk_data()
    elif use_case == "customer_support":
        from mock_data.customer_support import get_customer_support_data
        documents = get_customer_support_data()
    elif use_case == "hr_assistant":
        from mock_data.hr_assistant import get_hr_assistant_data
        documents = get_hr_assistant_data()
    else:
        raise ValueError(f"Unknown use case: {use_case}")

    # Create and initialize vector store
    vector_store = VectorStore(use_case)
    vector_store.create_index(documents, force_recreate)

    return vector_store


if __name__ == "__main__":
    # Test the vector store
    print("Testing Vector Store...")

    # Test IT Helpdesk use case
    vs = create_vector_store_for_use_case("it_helpdesk")

    # Test search
    results = vs.search("computer is slow", k=3)
    print(f"\nSearch results for 'computer is slow':")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result['score']:.3f}")
        print(f"   Content: {result['content'][:100]}...")
        print(f"   Category: {result['metadata'].get('category', 'N/A')}")

    # Print stats
    stats = vs.get_stats()
    print(f"\nVector Store Stats: {stats}")

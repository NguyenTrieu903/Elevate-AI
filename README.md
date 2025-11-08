# RAG Chatbot System

A comprehensive Retrieval-Augmented Generation (RAG) chatbot system built with Langchain, FAISS, and Azure OpenAI. This project demonstrates how to create intelligent chatbots that combine external knowledge retrieval with language generation for accurate, context-aware responses.

Link app: https://elevate-ai.streamlit.app/

## Features

- **Vector Database Integration**: FAISS for fast similarity search
- **RAG Pipeline**: Langchain for prompt chains and conversational flows
- **Function Calling**: Dynamic external data responses via Azure OpenAI
- **IT Helpdesk Use Case**: Technical troubleshooting and support
- **Mock Data Generation**: Synthetic datasets for testing and development

## Setup Instructions

### 1. Environment Setup

```bash
# Clone or download the project
cd ws4

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Azure OpenAI Configuration

1. Copy the environment template:

```bash
cp .env.template .env
```

2. Edit `.env` file with your Azure OpenAI credentials:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

### 3. Running the Chatbot

```bash
# Run the main chatbot
python chatbot_main.py

# Or run with Streamlit web interface
streamlit run streamlit_app.py

# Or use Jupyter notebook for interactive development
jupyter notebook demo_notebook.ipynb
```

## Project Structure

```
ws4/
├── chatbot_main.py          # Main chatbot application
├── streamlit_app.py         # Web interface using Streamlit
├── demo_notebook.ipynb      # Jupyter notebook demo
├── mock_data/
│   ├── __init__.py
│   ├── it_helpdesk.py      # IT helpdesk mock data
│   ├── customer_support.py # Customer support scenarios
│   └── hr_assistant.py     # HR assistant data
├── rag_system/
│   ├── __init__.py
│   ├── vector_store.py     # FAISS vector database
│   ├── retrieval_chain.py  # Langchain RAG chains
│   ├── function_calling.py # Azure OpenAI function calling
│   └── chat_interface.py   # Chat management
├── tests/
│   ├── __init__.py
│   ├── test_vector_store.py
│   ├── test_rag_chain.py
│   └── test_functions.py
├── requirements.txt
├── .env.template
└── README.md
```

## Use Cases

### 1. IT Helpdesk Troubleshooting Bot

- Diagnose common IT issues
- Search knowledge base for solutions
- System status checks via function calling

### 2. Customer Support FAQ Bot

- Handle customer inquiries
- Product information retrieval
- Order status and tracking

### 3. HR Assistant

- Employee onboarding guidance
- Policy and procedure queries
- Leave management assistance

## Example Usage

```python
from rag_system.chat_interface import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot(use_case="it_helpdesk")

# Start conversation
response = chatbot.chat("My computer is running very slow")
print(response)

# With function calling
response = chatbot.chat("Check status of printer01")
print(response)
```

## Testing

Run the test suite to validate functionality:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational purposes as part of the RAG Chatbot Workshop.

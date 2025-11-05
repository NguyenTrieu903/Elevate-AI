"""Streamlit web interface for RAG chatbot system."""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Load secrets from Streamlit Cloud (for production)
# Streamlit Cloud secrets are accessed via st.secrets
if hasattr(st, 'secrets') and st.secrets:
    # Map Streamlit secrets to environment variables
    secrets = st.secrets
    
    # LLM credentials
    if 'AZURE_OPENAI_LLM_ENDPOINT' in secrets:
        os.environ['AZURE_OPENAI_LLM_ENDPOINT'] = secrets['AZURE_OPENAI_LLM_ENDPOINT']
    if 'AZURE_OPENAI_LLM_API_KEY' in secrets:
        os.environ['AZURE_OPENAI_LLM_API_KEY'] = secrets['AZURE_OPENAI_LLM_API_KEY']
    if 'AZURE_OPENAI_LLM_MODEL' in secrets:
        os.environ['AZURE_OPENAI_LLM_MODEL'] = secrets['AZURE_OPENAI_LLM_MODEL']
    if 'AZURE_OPENAI_LLM_API_VERSION' in secrets:
        os.environ['AZURE_OPENAI_LLM_API_VERSION'] = secrets['AZURE_OPENAI_LLM_API_VERSION']
    
    # Embedding credentials
    if 'AZURE_OPENAI_EMBEDDING_ENDPOINT' in secrets:
        os.environ['AZURE_OPENAI_EMBEDDING_ENDPOINT'] = secrets['AZURE_OPENAI_EMBEDDING_ENDPOINT']
    if 'AZURE_OPENAI_EMBEDDING_API_KEY' in secrets:
        os.environ['AZURE_OPENAI_EMBEDDING_API_KEY'] = secrets['AZURE_OPENAI_EMBEDDING_API_KEY']
    if 'AZURE_OPENAI_EMBED_MODEL' in secrets:
        os.environ['AZURE_OPENAI_EMBED_MODEL'] = secrets['AZURE_OPENAI_EMBED_MODEL']
    if 'AZURE_OPENAI_EMBEDDING_API_VERSION' in secrets:
        os.environ['AZURE_OPENAI_EMBEDDING_API_VERSION'] = secrets['AZURE_OPENAI_EMBEDDING_API_VERSION']
    
    # Fallback to general credentials if specific ones not set
    if 'AZURE_OPENAI_ENDPOINT' in secrets:
        if 'AZURE_OPENAI_LLM_ENDPOINT' not in os.environ:
            os.environ['AZURE_OPENAI_LLM_ENDPOINT'] = secrets['AZURE_OPENAI_ENDPOINT']
        if 'AZURE_OPENAI_EMBEDDING_ENDPOINT' not in os.environ:
            os.environ['AZURE_OPENAI_EMBEDDING_ENDPOINT'] = secrets['AZURE_OPENAI_ENDPOINT']
    
    if 'AZURE_OPENAI_API_KEY' in secrets:
        if 'AZURE_OPENAI_LLM_API_KEY' not in os.environ:
            os.environ['AZURE_OPENAI_LLM_API_KEY'] = secrets['AZURE_OPENAI_API_KEY']
        if 'AZURE_OPENAI_EMBEDDING_API_KEY' not in os.environ:
            os.environ['AZURE_OPENAI_EMBEDDING_API_KEY'] = secrets['AZURE_OPENAI_API_KEY']
    
    if 'AZURE_OPENAI_API_VERSION' in secrets:
        if 'AZURE_OPENAI_LLM_API_VERSION' not in os.environ:
            os.environ['AZURE_OPENAI_LLM_API_VERSION'] = secrets['AZURE_OPENAI_API_VERSION']
        if 'AZURE_OPENAI_EMBEDDING_API_VERSION' not in os.environ:
            os.environ['AZURE_OPENAI_EMBEDDING_API_VERSION'] = secrets['AZURE_OPENAI_API_VERSION']

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from rag_system.chat_interface import RAGChatbot

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }

    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }

    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }

    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }

    .function-call-info {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }

    .sources-info {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'use_case' not in st.session_state:
        st.session_state.use_case = "it_helpdesk"

def create_chatbot(use_case: str, enable_functions: bool) -> RAGChatbot:
    """Create or recreate chatbot with specified settings."""
    try:
        return RAGChatbot(use_case=use_case, enable_functions=enable_functions)
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {str(e)}")
        
        # Check if we're on Streamlit Cloud
        if hasattr(st, 'secrets') and st.secrets:
            st.warning("""
            **Streamlit Cloud Configuration Required:**
            
            Please add your Azure OpenAI credentials to Streamlit Cloud Secrets:
            
            1. Go to your Streamlit Cloud dashboard
            2. Click on your app → Settings → Secrets
            3. Add the following secrets in TOML format:
            
            ```toml
            AZURE_OPENAI_LLM_ENDPOINT = "https://aiportalapi.stu-platform.live/jpe"
            AZURE_OPENAI_LLM_API_KEY = "your-llm-api-key"
            AZURE_OPENAI_LLM_MODEL = "GPT-4o-mini"
            AZURE_OPENAI_LLM_API_VERSION = "2024-02-15-preview"
            
            AZURE_OPENAI_EMBEDDING_ENDPOINT = "https://aiportalapi.stu-platform.live/jpe"
            AZURE_OPENAI_EMBEDDING_API_KEY = "your-embedding-api-key"
            AZURE_OPENAI_EMBED_MODEL = "text-embedding-3-small"
            AZURE_OPENAI_EMBEDDING_API_VERSION = "2024-02-15-preview"
            ```
            """)
        else:
            st.info("Please make sure your .env file is configured with Azure OpenAI credentials.")
        return None

def display_chat_message(message: dict, is_user: bool = True):
    """Display a chat message with appropriate styling."""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Assistant:</strong><br>
            {message['answer']}
        </div>
        """, unsafe_allow_html=True)

        # Show additional info
        if message.get('method') == 'function_calling' and message.get('function_calls_made', 0) > 0:
            st.markdown(f"""
            <div class="function-call-info">
                💡 <strong>Function Calls:</strong> Used {message['function_calls_made']} function call(s)
            </div>
            """, unsafe_allow_html=True)

        elif message.get('sources'):
            sources = ', '.join(message['sources'][:3])
            st.markdown(f"""
            <div class="sources-info">
                📚 <strong>Sources:</strong> {sources}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 RAG Chatbot System</h1>
        <p>Intelligent chatbots with retrieval-augmented generation and function calling</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")

    # Use case selection
    use_case = st.sidebar.selectbox(
        "Select Use Case:",
        ["it_helpdesk", "customer_support", "hr_assistant"],
        index=["it_helpdesk", "customer_support", "hr_assistant"].index(st.session_state.use_case),
        format_func=lambda x: {
            "it_helpdesk": "🔧 IT Helpdesk",
            "customer_support": "🛒 Customer Support",
            "hr_assistant": "👥 HR Assistant"
        }[x]
    )

    # Function calling toggle
    enable_functions = st.sidebar.checkbox("Enable Function Calling", value=True)

    # Initialize or recreate chatbot if settings changed
    if (st.session_state.chatbot is None or
        use_case != st.session_state.use_case):

        with st.spinner("Initializing chatbot..."):
            st.session_state.chatbot = create_chatbot(use_case, enable_functions)
            st.session_state.use_case = use_case
            st.session_state.chat_history = []  # Clear history on use case change

    if st.session_state.chatbot is None:
        return

    # Sidebar actions
    st.sidebar.header("🎮 Actions")

    if st.sidebar.button("🎬 Run Demo"):
        with st.spinner("Running demonstration..."):
            demo_questions = {
                "it_helpdesk": [
                    "My computer is running very slowly",
                    "What's the status of printer01?",
                    "How do I connect to the VPN?"
                ],
                "customer_support": [
                    "How can I track my order?",
                    "What's the status of order ORD123456?",
                    "Tell me about wireless headphones"
                ],
                "hr_assistant": [
                    "How do I request time off?",
                    "What's my leave balance for EMP001?",
                    "Tell me about health insurance"
                ]
            }

            questions = demo_questions.get(use_case, demo_questions["it_helpdesk"])

            for question in questions:
                # Add user message
                st.session_state.chat_history.append({
                    "content": question,
                    "is_user": True,
                    "timestamp": datetime.now()
                })

                # Get bot response
                response = st.session_state.chatbot.chat(question)
                st.session_state.chat_history.append({
                    **response,
                    "is_user": False,
                    "timestamp": datetime.now()
                })

    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        if st.session_state.chatbot:
            st.session_state.chatbot.clear_conversation()
        st.rerun()

    # Show chatbot statistics
    if st.sidebar.button("📊 Show Statistics"):
        if st.session_state.chatbot:
            stats = st.session_state.chatbot.get_chatbot_stats()
            st.sidebar.json(stats)

    # Available functions
    if st.session_state.chatbot and enable_functions:
        functions = st.session_state.chatbot.get_available_functions()
        if functions:
            st.sidebar.header("🔧 Available Functions")
            for func in functions:
                st.sidebar.text(f"• {func}")

    # Main chat interface
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("💬 Chat")

        # Chat history display
        chat_container = st.container()

        with chat_container:
            for message in st.session_state.chat_history:
                display_chat_message(message, message['is_user'])

        # Chat options
        col_options = st.columns(2)
        with col_options[0]:
            use_rag = st.checkbox("Use RAG", value=True)
        with col_options[1]:
            use_functions_input = st.checkbox("Use Functions", value=enable_functions)

        # Chat input form - supports both Enter key and Send button
        with st.form(key="chat_form", clear_on_submit=True):
            input_col, send_col = st.columns([5, 1])
            
            with input_col:
                user_input = st.text_input(
                    "Type your message:",
                    key="user_input",
                    placeholder="Ask me anything... (Press Enter or click Send)",
                    label_visibility="collapsed"
                )
            
            with send_col:
                st.write("")  # Spacing
                st.write("")  # Spacing
                send_button = st.form_submit_button("Send 📤", use_container_width=True)
        
        # Process user input when form is submitted (Enter key or Send button)
        if send_button and user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({
                "content": user_input,
                "is_user": True,
                "timestamp": datetime.now()
            })

            # Get bot response
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.chat(
                    user_input,
                    use_rag=use_rag,
                    use_functions=use_functions_input
                )

                st.session_state.chat_history.append({
                    **response,
                    "is_user": False,
                    "timestamp": datetime.now()
                })

            st.rerun()

    with col2:
        st.header("ℹ️ Information")

        # Use case description
        descriptions = {
            "it_helpdesk": """
            **IT Helpdesk Assistant**

            Helps with:
            - Technical troubleshooting
            - Device status checks
            - Software information
            - Network issues
            - Password resets
            """,
            "customer_support": """
            **Customer Support Bot**

            Helps with:
            - Order tracking
            - Product information
            - Shipping calculations
            - Returns & exchanges
            - Account management
            """,
            "hr_assistant": """
            **HR Assistant Bot**

            Helps with:
            - Leave requests
            - Benefits information
            - Company policies
            - Training courses
            - Holiday schedules
            """
        }

        st.markdown(descriptions.get(use_case, ""))

        # Recent activity
        if st.session_state.chat_history:
            st.subheader("📈 Recent Activity")
            recent_count = len(st.session_state.chat_history)
            user_count = len([m for m in st.session_state.chat_history if m['is_user']])
            bot_count = recent_count - user_count

            st.metric("Total Messages", recent_count)
            st.metric("User Messages", user_count)
            st.metric("Bot Responses", bot_count)

if __name__ == "__main__":
    main()

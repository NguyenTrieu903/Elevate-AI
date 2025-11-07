"""Streamlit web interface for RAG chatbot system."""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Load secrets from Streamlit Cloud (for production) safely
# Accessing st.secrets when no secrets file exists may raise an error; guard it.
try:
    has_secrets = False
    secrets_file_exists = any([
        (Path.home() / ".streamlit/secrets.toml").exists(),
        (Path(__file__).parent / ".streamlit/secrets.toml").exists(),
    ])
    if secrets_file_exists and hasattr(st, 'secrets'):
        has_secrets = True
    
    if has_secrets:
        secrets = st.secrets  # type: ignore

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
except Exception:
    # If anything goes wrong with secrets loading, continue with .env only
    pass

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from rag_system.chat_interface import RAGChatbot
from rag_system.text_to_speech import synthesize_to_mp3_bytes

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
    
    /* Improve chat interface spacing and scrolling */
    .stChatMessage {
        padding: 1rem;
    }
    
    /* Ensure chat input stays at bottom */
    [data-testid="stChatInput"] {
        position: sticky;
        bottom: 0;
        background-color: white;
        z-index: 100;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Smooth scrolling for chat messages */
    .element-container:has([data-testid="stChatMessage"]) {
        scroll-behavior: smooth;
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
    if 'in_demo' not in st.session_state:
        st.session_state.in_demo = False

# -----------------------------
# TTS helpers (cached + concurrent)
# -----------------------------
from concurrent.futures import ThreadPoolExecutor, as_completed

@st.cache_data(show_spinner=False)
def _cached_tts(text: str, lang: str) -> bytes | None:
    return synthesize_to_mp3_bytes(text, lang)

def generate_tts_concurrently(items: list[tuple[int, str]], lang: str, workers: int = 4) -> dict[int, bytes]:
    """Generate TTS for multiple texts in parallel.

    items: list of (message_index, text)
    returns: mapping index -> audio bytes (only successful ones)
    """
    results: dict[int, bytes] = {}
    if not items:
        return results
    progress = st.progress(0, text="Generating audio...")
    total = len(items)
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        futures = {ex.submit(_cached_tts, text[:4000], lang): idx for idx, text in items}
        done_count = 0
        for fut in as_completed(futures):
            idx = futures[fut]
            try:
                data = fut.result()
                if data:
                    results[idx] = data
            except Exception:
                pass
            done_count += 1
            progress.progress(min(1.0, done_count / total))
    progress.empty()
    return results

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

def display_chat_message(message: dict, index: int = 0):
    """Display a chat message using Streamlit's native chat components."""
    is_user = message.get('is_user', False)
    
    if is_user:
        with st.chat_message("user"):
            st.write(message.get('content', ''))
    else:
        with st.chat_message("assistant"):
            # Main response
            st.write(message.get('answer', ''))
            
            # Show additional info
            if message.get('method') == 'function_calling' and message.get('function_calls_made', 0) > 0:
                st.info(f"💡 Used {message['function_calls_made']} function call(s)")
            
            elif message.get('sources'):
                sources = ', '.join(message['sources'][:3])
                st.caption(f"📚 Sources: {sources}")
            
            # Audio playback if available
            if message.get("audio"):
                st.audio(message["audio"], format=message.get("audio_mime", "audio/mp3"))
            elif not st.session_state.get("in_demo", False):
                # Show play button for on-demand TTS if TTS wasn't auto-generated
                play_key = f"play_tts_{index}"
                if st.button("🔊 Play Audio", key=play_key):
                    lang = st.session_state.get("tts_lang", "en")
                    to_say = (message.get("answer", "") or "")[:4000]
                    audio_bytes = synthesize_to_mp3_bytes(to_say, lang=lang)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        # Store audio in message for future renders
                        message["audio"] = audio_bytes
                        message["audio_mime"] = "audio/mp3"
                    else:
                        st.warning("TTS failed to generate audio. Please check your network and try again.")

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

    # Default TTS language (no Play button in UI; demo will auto-generate audio)
    st.session_state["tts_lang"] = st.session_state.get("tts_lang", "en")

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
        st.session_state.in_demo = True
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
        
        # Clear existing chat for demo
        st.session_state.chat_history = []
        
        # Process demo questions
        ai_indices: list[int] = []
        pending_texts: list[tuple[int, str]] = []
        
        for question in questions:
            # Add user message
            user_msg = {
                "content": question,
                "is_user": True,
                "timestamp": datetime.now()
            }
            st.session_state.chat_history.append(user_msg)

            # Get bot response
            with st.spinner(f"Processing: {question[:50]}..."):
                response = st.session_state.chatbot.chat(question)
            
            message_record = {**response, "is_user": False, "timestamp": datetime.now()}
            st.session_state.chat_history.append(message_record)
            ai_index = len(st.session_state.chat_history) - 1
            ai_indices.append(ai_index)
            pending_texts.append((ai_index, response.get("answer", "") or ""))

        # Generate TTS in parallel after all responses
        lang = st.session_state.get("tts_lang", "en")
        if pending_texts:
            audio_map = generate_tts_concurrently(pending_texts, lang)
            for idx, audio_bytes in audio_map.items():
                st.session_state.chat_history[idx]["audio"] = audio_bytes
                st.session_state.chat_history[idx]["audio_mime"] = "audio/mp3"

        # Demo finished
        st.session_state.in_demo = False
        st.rerun()

    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        if st.session_state.chatbot:
            st.session_state.chatbot.clear_conversation()
        st.success("Chat cleared!")
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

        # Display chat history
        for idx, message in enumerate(st.session_state.chat_history):
            display_chat_message(message, idx)

        # Chat options
        with st.expander("⚙️ Chat Options", expanded=False):
            col_options = st.columns(2)
            with col_options[0]:
                use_rag = st.checkbox("Use RAG", value=True, key="use_rag")
            with col_options[1]:
                use_functions_input = st.checkbox("Use Functions", value=enable_functions, key="use_functions")

            # TTS controls for normal chat; auto-enabled during demo
            tts_enable_user = st.checkbox("🔊 Enable Text-to-Speech", value=False, key="tts_enable")
            tts_lang = st.selectbox(
                "TTS Language",
                ["en", "vi"],
                index=["en", "vi"].index(st.session_state.get("tts_lang", "en")),
                key="tts_lang_select"
            )
            st.session_state["tts_lang"] = tts_lang
            # If demo is running, force-enable TTS regardless of checkbox
            tts_enable = bool(st.session_state.get("in_demo", False) or tts_enable_user)

        # Chat input - uses Streamlit's native chat_input which handles Enter key automatically
        if prompt := st.chat_input("Ask me anything..."):
            # Display user message immediately (like ChatGPT) - appears instantly
            with st.chat_message("user"):
                st.write(prompt)
            
            # Add user message to history immediately
            user_message = {
                "content": prompt,
                "is_user": True,
                "timestamp": datetime.now()
            }
            st.session_state.chat_history.append(user_message)
            
            # Show assistant message with typing indicator (like ChatGPT)
            with st.chat_message("assistant"):
                # Create a placeholder for the response
                message_placeholder = st.empty()
                
                # Show typing indicator (ChatGPT-style)
                with message_placeholder.container():
                    st.markdown("_Thinking..._")
                
                # Generate bot response
                response = st.session_state.chatbot.chat(
                    prompt,
                    use_rag=use_rag,
                    use_functions=use_functions_input
                )
                
                # Replace typing indicator with actual response
                with message_placeholder.container():
                    st.write(response.get('answer', ''))
                
                # Show additional info below the response
                if response.get('method') == 'function_calling' and response.get('function_calls_made', 0) > 0:
                    st.info(f"💡 Used {response['function_calls_made']} function call(s)")
                
                elif response.get('sources'):
                    sources = ', '.join(response['sources'][:3])
                    st.caption(f"📚 Sources: {sources}")
                
                # Optionally synthesize TTS
                if tts_enable and response.get("answer"):
                    to_say = (response.get("answer", "") or "")[:4000]
                    audio_bytes = synthesize_to_mp3_bytes(to_say, lang=tts_lang)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        response["audio"] = audio_bytes
                        response["audio_mime"] = "audio/mp3"
            
            # Add bot response to history
            message_record = {
                **response,
                "is_user": False,
                "timestamp": datetime.now()
            }
            st.session_state.chat_history.append(message_record)
            
            # Rerun to sync everything and prepare for next input
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

"""Streamlit web interface for RAG chatbot system."""

import streamlit as st
import sys
import os
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
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
    
    /* Dark mode styles */
    .dark-mode {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Keyboard shortcuts hint */
    .shortcuts-hint {
        font-size: 0.8rem;
        color: #666;
        padding: 0.5rem;
        background-color: #f5f5f5;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Keyboard shortcuts info
KEYBOARD_SHORTCUTS = """
**Keyboard Shortcuts:**
- `Enter` - Send message
- `Shift + Enter` - New line
- `Ctrl/Cmd + K` - Focus search
- `Ctrl/Cmd + /` - Show shortcuts
"""

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
    if 'conversation_threads' not in st.session_state:
        st.session_state.conversation_threads = {"default": {
            "name": "Default Conversation",
            "history": [],
            "created_at": datetime.now().isoformat()
        }}
    if 'current_thread_id' not in st.session_state:
        st.session_state.current_thread_id = "default"
    if 'message_ratings' not in st.session_state:
        st.session_state.message_ratings = {}
    if 'editing_message_id' not in st.session_state:
        st.session_state.editing_message_id = None
    if 'regenerating_message_id' not in st.session_state:
        st.session_state.regenerating_message_id = None
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'advanced_settings' not in st.session_state:
        st.session_state.advanced_settings = {
            'temperature': 0.7,
            'max_tokens': None,
            'top_p': 1.0
        }

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

# -----------------------------
# Export/Import utilities
# -----------------------------
def _convert_datetime_to_str(obj, is_audio=False):
    """Recursively convert datetime objects to ISO format strings and bytes to base64.
    
    Args:
        obj: Object to convert
        is_audio: Whether this is audio data (to mark it for later decoding)
    """
    try:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            # Convert bytes to base64 string for JSON serialization
            # Mark audio bytes so we can decode them later
            if is_audio:
                return {
                    "_type": "base64_audio",
                    "data": base64.b64encode(obj).decode('utf-8')
                }
            else:
                return base64.b64encode(obj).decode('utf-8')
        elif isinstance(obj, dict):
            # Don't recurse into our own marker dicts
            if obj.get("_type") == "base64_audio":
                return obj
            # Check if this dict contains audio field
            is_audio_field = "audio" in obj
            return {
                key: _convert_datetime_to_str(value, is_audio=(is_audio_field and key == "audio"))
                for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [_convert_datetime_to_str(item, is_audio) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(_convert_datetime_to_str(item, is_audio) for item in obj)
        else:
            return obj
    except Exception as e:
        # If conversion fails, return None to avoid breaking export
        # This handles any unexpected types gracefully
        return None

def export_chat_history(chat_history: List[Dict]) -> str:
    """Export chat history to JSON string."""
    # Convert datetime objects to strings before serialization
    serializable_history = _convert_datetime_to_str(chat_history)
    
    export_data = {
        "export_date": datetime.now().isoformat(),
        "chat_history": serializable_history,
        "version": "1.0"
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def import_chat_history(json_str: str) -> List[Dict]:
    """Import chat history from JSON string."""
    try:
        data = json.loads(json_str)
        if isinstance(data, dict) and "chat_history" in data:
            return data["chat_history"]
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        st.error(f"Failed to import chat history: {str(e)}")
        return []

def get_download_link(data: str, filename: str, mime: str = "application/json"):
    """Generate download link for data."""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# -----------------------------
# Chatbot creation
# -----------------------------
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
    """Display a chat message using Streamlit's native chat components with enhanced features."""
    is_user = message.get('is_user', False)
    message_id = f"msg_{index}"
    
    if is_user:
        with st.chat_message("user"):
            # Check if editing this message
            if st.session_state.get('editing_message_id') == message_id:
                edited_text = st.text_area(
                    "Edit message:",
                    value=message.get('content', ''),
                    key=f"edit_input_{index}",
                    height=100
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✓ Save", key=f"save_edit_{index}"):
                        message['content'] = edited_text
                        st.session_state.editing_message_id = None
                        # Regenerate response if there's a following assistant message
                        if index + 1 < len(st.session_state.chat_history):
                            st.session_state.regenerating_message_id = f"msg_{index + 1}"
                        st.rerun()
                with col2:
                    if st.button("✗ Cancel", key=f"cancel_edit_{index}"):
                        st.session_state.editing_message_id = None
                        st.rerun()
            else:
                st.write(message.get('content', ''))
                # Action buttons for user messages
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("✏️ Edit", key=f"edit_btn_{index}"):
                        st.session_state.editing_message_id = message_id
                        st.rerun()
                with col2:
                    if st.button("📋 Copy", key=f"copy_user_{index}"):
                        st.write("```\n" + message.get('content', '') + "\n```")
                        st.success("Message copied! (Use Ctrl+C)")
                with col3:
                    if st.button("🔄 Regenerate", key=f"regen_user_{index}"):
                        # Remove this message and regenerate
                        st.session_state.chat_history = st.session_state.chat_history[:index]
                        if st.session_state.chatbot:
                            st.session_state.chatbot.clear_conversation()
                            # Rebuild conversation history
                            for i in range(0, index, 2):
                                if i + 1 < len(st.session_state.chat_history):
                                    user_msg = st.session_state.chat_history[i]
                                    bot_msg = st.session_state.chat_history[i + 1]
                                    st.session_state.chatbot.conversation_manager.add_exchange(
                                        user_msg.get('content', ''),
                                        bot_msg.get('answer', '')
                                    )
                        st.rerun()
    else:
        with st.chat_message("assistant"):
            # Check if regenerating this message
            if st.session_state.get('regenerating_message_id') == message_id:
                with st.spinner("Regenerating response..."):
                    # Get the previous user message
                    if index > 0:
                        prev_message = st.session_state.chat_history[index - 1]
                        if prev_message.get('is_user'):
                            # Always use RAG, no function calling
                            response = st.session_state.chatbot.chat(
                                prev_message.get('content', ''),
                                use_rag=True,
                                use_functions=False
                            )
                            # Update message
                            message.update({
                                **response,
                                "is_user": False,
                                "timestamp": datetime.now()
                            })
                            st.session_state.regenerating_message_id = None
                            st.rerun()
            
            # Main response
            st.write(message.get('answer', ''))
            
            # Show additional info (RAG only)
            if message.get('method') == 'rag_retrieval':
                # Show RAG indicator
                retrieved_count = len(message.get('retrieved_documents', []))
                if retrieved_count > 0:
                    st.success(f"✅ Using RAG - Retrieved {retrieved_count} document(s) from knowledge base")
                if message.get('sources'):
                    sources = ', '.join(message['sources'][:3])
                    st.caption(f"📚 Sources: {sources}")
            
            # Action buttons row
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                # Rating buttons
                rating_key = f"rating_{index}"
                current_rating = st.session_state.message_ratings.get(message_id, None)
                
                if current_rating == "up":
                    st.button("👍", key=f"thumb_up_{index}", disabled=True)
                else:
                    if st.button("👍", key=f"thumb_up_{index}"):
                        st.session_state.message_ratings[message_id] = "up"
                        st.rerun()
            
            with col2:
                if current_rating == "down":
                    st.button("👎", key=f"thumb_down_{index}", disabled=True)
                else:
                    if st.button("👎", key=f"thumb_down_{index}"):
                        st.session_state.message_ratings[message_id] = "down"
                        st.rerun()
            
            with col3:
                if st.button("🔄", key=f"regen_{index}", help="Regenerate response"):
                    st.session_state.regenerating_message_id = message_id
                    st.rerun()
            
            with col4:
                if st.button("📋", key=f"copy_{index}", help="Copy message"):
                    st.code(message.get('answer', ''), language=None)
                    st.success("Message copied! (Use Ctrl+C)")
            
            with col5:
                if st.button("🔊", key=f"audio_btn_{index}", help="Play audio"):
                    lang = st.session_state.get("tts_lang", "en")
                    to_say = (message.get("answer", "") or "")[:4000]
                    audio_bytes = synthesize_to_mp3_bytes(to_say, lang=lang)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                        message["audio"] = audio_bytes
                        message["audio_mime"] = "audio/mp3"
                    else:
                        st.warning("TTS failed to generate audio.")
            
            # Audio playback if available
            audio_data = message.get("audio")
            if audio_data:
                # Check if audio is base64 encoded (from loaded conversation)
                if isinstance(audio_data, dict) and audio_data.get("_type") == "base64_audio":
                    try:
                        # Decode base64 string back to bytes
                        audio_bytes = base64.b64decode(audio_data["data"])
                        st.audio(audio_bytes, format=message.get("audio_mime", "audio/mp3"))
                    except Exception as e:
                        st.warning(f"Failed to decode audio: {str(e)}")
                elif isinstance(audio_data, bytes):
                    # Fresh audio bytes (not yet serialized)
                    st.audio(audio_data, format=message.get("audio_mime", "audio/mp3"))
                elif isinstance(audio_data, str):
                    # Try to decode if it's a base64 string (fallback for old format)
                    try:
                        audio_bytes = base64.b64decode(audio_data)
                        st.audio(audio_bytes, format=message.get("audio_mime", "audio/mp3"))
                    except Exception:
                        st.warning("Audio data format not recognized")

def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 RAG Chatbot System</h1>
        <p>Intelligent chatbot with retrieval-augmented generation</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")

    # Use case selection (IT Helpdesk only)
    use_case = "it_helpdesk"
    st.session_state.use_case = use_case

    # Default TTS language (no Play button in UI; demo will auto-generate audio)
    st.session_state["tts_lang"] = st.session_state.get("tts_lang", "en")

    # Initialize or recreate chatbot if settings changed
    # Always use RAG only (no function calling)
    if (st.session_state.chatbot is None or
        use_case != st.session_state.use_case):

        with st.spinner("Initializing chatbot..."):
            st.session_state.chatbot = create_chatbot(use_case, enable_functions=False)
            st.session_state.use_case = use_case
            st.session_state.chat_history = []  # Clear history on use case change

    if st.session_state.chatbot is None:
        return

    # Advanced Settings
    with st.sidebar.expander("⚙️ Advanced Settings", expanded=False):
        st.session_state.advanced_settings['temperature'] = st.slider(
            "Temperature", 0.0, 2.0, st.session_state.advanced_settings['temperature'], 0.1,
            help="Controls randomness. Lower = more focused, Higher = more creative"
        )
        st.session_state.advanced_settings['max_tokens'] = st.number_input(
            "Max Tokens", min_value=100, max_value=4000, value=2000, step=100,
            help="Maximum tokens in response"
        )
        st.session_state.advanced_settings['top_p'] = st.slider(
            "Top P", 0.0, 1.0, st.session_state.advanced_settings['top_p'], 0.1,
            help="Nucleus sampling parameter"
        )
    
    # Dark Mode Toggle
    st.sidebar.markdown("---")
    dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        if dark_mode:
            st.markdown("""
            <style>
                .stApp {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
            </style>
            """, unsafe_allow_html=True)
    
    # Export/Import Chat History
    st.sidebar.markdown("---")
    st.sidebar.header("💾 Chat History")
    
    # Export button
    if st.session_state.chat_history:
        export_json = export_chat_history(st.session_state.chat_history)
        st.sidebar.download_button(
            label="📥 Export Chat History",
            data=export_json,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.sidebar.info("No chat history to export")
    
    # Import button
    uploaded_file = st.sidebar.file_uploader(
        "📤 Import Chat History",
        type=['json'],
        key="import_file",
        help="Upload a JSON file to restore chat history"
    )
    if uploaded_file is not None:
        json_str = uploaded_file.read().decode('utf-8')
        imported_history = import_chat_history(json_str)
        if imported_history:
            st.session_state.chat_history = imported_history
            st.sidebar.success(f"✅ Imported {len(imported_history)} messages")
            st.rerun()
    
    # Search in Chat History
    st.sidebar.markdown("---")
    search_query = st.sidebar.text_input("🔍 Search in Chat", placeholder="Search messages...")
    if search_query:
        filtered_history = []
        for idx, msg in enumerate(st.session_state.chat_history):
            content = msg.get('content', '') if msg.get('is_user') else msg.get('answer', '')
            if search_query.lower() in content.lower():
                filtered_history.append((idx, msg))
        if filtered_history:
            st.sidebar.write(f"Found {len(filtered_history)} matches")
            for idx, msg in filtered_history[:5]:  # Show first 5 matches
                preview = (msg.get('content', '') if msg.get('is_user') else msg.get('answer', ''))[:50]
                if st.sidebar.button(f"→ {preview}...", key=f"search_result_{idx}"):
                    # Scroll to message (would need JS, but we can highlight it)
                    st.session_state.highlight_message = idx
                    st.rerun()
        else:
            st.sidebar.info("No matches found")
    
    # Conversation Threads
    st.sidebar.markdown("---")
    st.sidebar.header("💬 Conversations")
    
    # Create new thread
    if st.sidebar.button("➕ New Conversation"):
        # Save current thread before creating new one
        if st.session_state.chat_history and st.session_state.current_thread_id:
            # Convert datetime objects to strings before saving
            serializable_history = _convert_datetime_to_str(st.session_state.chat_history.copy())
            st.session_state.conversation_threads[st.session_state.current_thread_id] = {
                "name": st.session_state.conversation_threads.get(
                    st.session_state.current_thread_id, {}
                ).get("name", "Current Conversation"),
                "history": serializable_history,
                "updated_at": datetime.now().isoformat()
            }
        
        thread_id = f"thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.conversation_threads[thread_id] = {
            "name": f"Conversation {len(st.session_state.conversation_threads) + 1}",
            "history": [],
            "created_at": datetime.now().isoformat()
        }
        st.session_state.current_thread_id = thread_id
        st.session_state.chat_history = []
        if st.session_state.chatbot:
            st.session_state.chatbot.clear_conversation()
        st.rerun()
    
    # List existing threads
    if st.session_state.conversation_threads:
        for thread_id, thread_data in list(st.session_state.conversation_threads.items())[-5:]:
            thread_name = thread_data.get("name", thread_id)
            is_current = thread_id == st.session_state.current_thread_id
            if st.sidebar.button(
                f"{'▶️' if is_current else '○'} {thread_name}",
                key=f"thread_{thread_id}",
                use_container_width=True
            ):
                if not is_current:
                    # Save current thread (convert datetime to strings)
                    if st.session_state.chat_history:
                        serializable_history = _convert_datetime_to_str(st.session_state.chat_history.copy())
                        st.session_state.conversation_threads[st.session_state.current_thread_id] = {
                            "name": st.session_state.conversation_threads.get(
                                st.session_state.current_thread_id, {}
                            ).get("name", "Current Conversation"),
                            "history": serializable_history,
                            "updated_at": datetime.now().isoformat()
                        }
                    
                    # Load selected thread
                    st.session_state.current_thread_id = thread_id
                    # Thread history is already serialized (strings), so we can use it directly
                    st.session_state.chat_history = thread_data.get("history", []).copy()
                    # Rebuild conversation history in chatbot
                    if st.session_state.chatbot:
                        st.session_state.chatbot.clear_conversation()
                        for i in range(0, len(st.session_state.chat_history), 2):
                            if i + 1 < len(st.session_state.chat_history):
                                user_msg = st.session_state.chat_history[i]
                                bot_msg = st.session_state.chat_history[i + 1]
                                if user_msg.get('is_user') and not bot_msg.get('is_user'):
                                    st.session_state.chatbot.conversation_manager.add_exchange(
                                        user_msg.get('content', ''),
                                        bot_msg.get('answer', '')
                                    )
                    st.rerun()
    
    # Save current thread (convert datetime to strings)
    if st.session_state.chat_history and st.session_state.current_thread_id:
        serializable_history = _convert_datetime_to_str(st.session_state.chat_history.copy())
        st.session_state.conversation_threads[st.session_state.current_thread_id] = {
            "name": st.session_state.conversation_threads.get(
                st.session_state.current_thread_id, {}
            ).get("name", "Current Conversation"),
            "history": serializable_history,
            "updated_at": datetime.now().isoformat()
        }

    # Keyboard shortcuts info
    with st.sidebar.expander("⌨️ Keyboard Shortcuts", expanded=False):
        st.markdown(KEYBOARD_SHORTCUTS)
    
    # Sidebar actions
    st.sidebar.markdown("---")
    st.sidebar.header("🎮 Actions")

    if st.sidebar.button("🎬 Run Demo"):
        st.session_state.in_demo = True
        demo_questions = [
            "My computer is running very slowly",
            "What's the status of printer01?",
            "How do I connect to the VPN?"
        ]

        questions = demo_questions
        
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

    # RAG is always used, no function calling

    # Main chat interface
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("💬 Chat")

        # Display chat history with search highlighting
        highlight_idx = st.session_state.get('highlight_message', None)
        for idx, message in enumerate(st.session_state.chat_history):
            # Highlight message if it matches search
            if highlight_idx == idx:
                st.markdown("""
                <div style="border: 2px solid #ff6b6b; border-radius: 10px; padding: 10px; margin: 10px 0;">
                """, unsafe_allow_html=True)
                display_chat_message(message, idx)
                st.markdown("</div>", unsafe_allow_html=True)
                # Clear highlight after showing
                if 'highlight_message' in st.session_state:
                    del st.session_state.highlight_message
            else:
                display_chat_message(message, idx)

        # Chat options
        with st.expander("⚙️ Chat Options", expanded=False):
            # RAG is always enabled
            use_rag = True
            use_functions_input = False
            st.info("ℹ️ RAG is always enabled for knowledge base retrieval")

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
                
                # Show additional info below the response (RAG only)
                if response.get('method') == 'rag_retrieval':
                    # Show RAG indicator
                    retrieved_count = len(response.get('retrieved_documents', []))
                    if retrieved_count > 0:
                        st.success(f"✅ Using RAG - Retrieved {retrieved_count} document(s) from knowledge base")
                    if response.get('sources'):
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
        description = """
        **IT Helpdesk Assistant**

        Helps with:
        - Technical troubleshooting
        - Device status checks
        - Software information
        - Network issues
        - Password resets
        """

        st.markdown(description)

        # Enhanced Analytics Dashboard
        if st.session_state.chat_history:
            st.subheader("📊 Conversation Analytics")
            
            recent_count = len(st.session_state.chat_history)
            user_count = len([m for m in st.session_state.chat_history if m['is_user']])
            bot_count = recent_count - user_count
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("Total Messages", recent_count)
            with col_met2:
                st.metric("Exchanges", bot_count)
            
            # Response ratings analytics
            ratings = st.session_state.message_ratings
            if ratings:
                up_votes = sum(1 for r in ratings.values() if r == "up")
                down_votes = sum(1 for r in ratings.values() if r == "down")
                st.metric("👍 Positive", up_votes)
                st.metric("👎 Negative", down_votes)
            
            # Method distribution
            methods = {}
            for msg in st.session_state.chat_history:
                if not msg.get('is_user'):
                    method = msg.get('method', 'unknown')
                    methods[method] = methods.get(method, 0) + 1
            
            if methods:
                st.subheader("Response Methods")
                for method, count in methods.items():
                    method_name = method.replace('_', ' ').title()
                    st.progress(count / bot_count if bot_count > 0 else 0, text=f"{method_name}: {count}")
            
            # Average response length
            if bot_count > 0:
                avg_length = sum(
                    len(msg.get('answer', '')) 
                    for msg in st.session_state.chat_history 
                    if not msg.get('is_user')
                ) / bot_count
                st.metric("Avg Response Length", f"{int(avg_length)} chars")
            
            # Conversation threads info
            if st.session_state.conversation_threads:
                st.subheader("💬 Threads")
                st.metric("Active Threads", len(st.session_state.conversation_threads))
        else:
            st.info("Start chatting to see analytics!")

if __name__ == "__main__":
    main()

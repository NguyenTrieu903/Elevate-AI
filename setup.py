"""Setup script to initialize the RAG chatbot system."""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected.")
    return True

def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_environment():
    """Set up environment configuration."""
    env_template = Path(".env.template")
    env_file = Path(".env")

    if not env_template.exists():
        print("❌ .env.template file not found.")
        return False

    if env_file.exists():
        print("⚠️ .env file already exists. Skipping creation.")
        return True

    try:
        # Copy template to .env
        with open(env_template, 'r') as template:
            content = template.read()

        with open(env_file, 'w') as env:
            env.write(content)

        print("✅ .env file created from template.")
        print("⚠️ Please edit .env file with your Azure OpenAI credentials.")
        return True

    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        "vector_indexes",
        "logs"
    ]

    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"✅ Created directory: {dir_name}")
        else:
            print(f"📁 Directory already exists: {dir_name}")

def validate_setup():
    """Validate the setup by importing key modules."""
    print("🔍 Validating setup...")

    try:
        # Test imports without initializing (to avoid API calls)
        from rag_system.vector_store import VectorStore
        from rag_system.function_calling import FunctionCaller
        from rag_system.retrieval_chain import RetrievalChain
        from rag_system.chat_interface import RAGChatbot
        from mock_data.it_helpdesk import get_it_helpdesk_data

        print("✅ All modules imported successfully.")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing missing dependencies with: pip install -r requirements.txt")
        return False

def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 RAG Chatbot System Setup Complete!")
    print("=" * 60)

    print("\n📋 Next Steps:")
    print("1. Configure your Azure OpenAI credentials in .env file")
    print("2. Test the setup with: python -c \"from rag_system.chat_interface import RAGChatbot; print('Setup OK!')\"")
    print("3. Run the command-line interface: python chatbot_main.py")
    print("4. Launch the web interface: streamlit run streamlit_app.py")
    print("5. Explore the Jupyter notebook: jupyter notebook demo_notebook.ipynb")

    print("\n🧪 Testing:")
    print("• Run all tests: python run_tests.py")
    print("• Run specific tests: python -m pytest tests/test_vector_store.py -v")

    print("\n📚 Documentation:")
    print("• README.md - Complete setup and usage guide")
    print("• demo_notebook.ipynb - Interactive demonstration")
    print("• .env.template - Environment configuration template")

    print("\n🔧 Available Use Cases:")
    print("• IT Helpdesk: python chatbot_main.py --use-case it_helpdesk")
    print("• Customer Support: python chatbot_main.py --use-case customer_support")
    print("• HR Assistant: python chatbot_main.py --use-case hr_assistant")

def main():
    """Main setup function."""
    print("🚀 Setting up RAG Chatbot System...")
    print("=" * 50)

    # Check Python version
    if not check_python_version():
        return 1

    # Install requirements
    if not install_requirements():
        print("⚠️ Requirements installation failed. You may need to install manually.")

    # Setup environment
    if not setup_environment():
        return 1

    # Create directories
    create_directories()

    # Validate setup
    if not validate_setup():
        print("\n⚠️ Setup validation failed. Please check error messages above.")
        return 1

    # Display next steps
    display_next_steps()

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

"""Main chatbot application with command-line interface."""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from rag_system.chat_interface import ChatInterface, RAGChatbot
from dotenv import load_dotenv

def check_environment():
    """Check if environment variables are properly configured."""
    load_dotenv()

    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please copy .env.template to .env and fill in your Azure OpenAI credentials.")
        return False

    print("✅ Environment variables configured correctly.")
    return True

def main():
    """Main function to run the chatbot."""
    parser = argparse.ArgumentParser(description="RAG Chatbot System")
    parser.add_argument(
        "--use-case",
        choices=["it_helpdesk", "customer_support", "hr_assistant"],
        default="it_helpdesk",
        help="Choose the chatbot use case (default: it_helpdesk)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration mode"
    )
    parser.add_argument(
        "--no-functions",
        action="store_true",
        help="Disable function calling (RAG only)"
    )

    args = parser.parse_args()

    # Check environment configuration
    if not check_environment():
        return 1

    try:
        print(f"🚀 Starting RAG Chatbot System...")
        print(f"📋 Use Case: {args.use_case}")

        if args.demo:
            # Run demonstration mode
            print("🎬 Running in demonstration mode...")
            chatbot = RAGChatbot(
                use_case=args.use_case,
                enable_functions=not args.no_functions
            )
            chatbot.demo_interaction()
        else:
            # Run interactive chat interface
            interface = ChatInterface(args.use_case)
            interface.run()

        return 0

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Make sure you have installed all requirements and configured your .env file.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

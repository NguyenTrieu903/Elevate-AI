"""Chat interface integrating RAG and function calling."""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from .retrieval_chain import RetrievalChain, ConversationManager
from .function_calling import FunctionCaller
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGChatbot:
    """Complete RAG chatbot with retrieval and function calling."""

    def __init__(self, use_case: str = "it_helpdesk", enable_functions: bool = True):
        """Initialize RAG chatbot.

        Args:
            use_case: The use case (it_helpdesk, customer_support, hr_assistant)
            enable_functions: Whether to enable function calling
        """
        self.use_case = use_case
        self.enable_functions = enable_functions

        # Initialize components
        self.retrieval_chain = RetrievalChain(use_case)
        self.conversation_manager = ConversationManager()

        if enable_functions:
            self.function_caller = FunctionCaller(use_case)
        else:
            self.function_caller = None

        print(f"RAG Chatbot initialized for {use_case}")
        if enable_functions:
            print(f"Function calling enabled with {len(self.function_caller.functions)} functions")

    def chat(self, user_input: str, use_rag: bool = True, use_functions: bool = True) -> Dict[str, Any]:
        """Process user input with RAG and/or function calling.

        Args:
            user_input: User's message
            use_rag: Whether to use RAG retrieval
            use_functions: Whether to use function calling

        Returns:
            Complete response with all components
        """
        response = {
            "user_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "use_case": self.use_case
        }

        try:
            if use_functions and self.function_caller:
                # Try function calling first
                messages = [
                    {"role": "system", "content": self._get_system_message()},
                    *self._format_chat_history(),
                    {"role": "user", "content": user_input}
                ]

                func_result = self.function_caller.chat_with_functions(messages)

                if "content" in func_result and func_result["content"]:
                    # Function calling provided a response
                    response.update({
                        "answer": func_result["content"],
                        "method": "function_calling",
                        "function_calls_made": func_result.get("function_calls_made", 0),
                        "success": True
                    })

                    # Add to conversation history
                    self.conversation_manager.add_exchange(user_input, func_result["content"])

                    return response

            if use_rag:
                # Use RAG retrieval and generation
                rag_result = self.retrieval_chain.chat(
                    user_input,
                    self.conversation_manager.get_history()
                )

                response.update({
                    "answer": rag_result["answer"],
                    "method": "rag_retrieval",
                    "retrieved_documents": rag_result["retrieved_documents"],
                    "sources": rag_result["sources"],
                    "success": True
                })

                # Add to conversation history
                self.conversation_manager.add_exchange(user_input, rag_result["answer"])

            else:
                # Fallback response
                response.update({
                    "answer": "I'm sorry, I need to have either RAG or function calling enabled to assist you.",
                    "method": "fallback",
                    "success": False
                })

        except Exception as e:
            response.update({
                "answer": f"I encountered an error processing your request: {str(e)}",
                "method": "error",
                "error": str(e),
                "success": False
            })

        return response

    def _get_system_message(self) -> str:
        """Get system message based on use case."""
        system_messages = {
            "it_helpdesk": "You are an experienced IT helpdesk assistant. Help users with technical problems, device status checks, and software information. Use available functions when needed to provide accurate information.",

            "customer_support": "You are a friendly customer support representative. Help customers with orders, products, shipping, and account issues. Use available functions to check real-time information when appropriate.",

            "hr_assistant": "You are a knowledgeable HR assistant. Help employees with benefits, leave requests, company policies, and training information. Use available functions to access employee-specific data when needed."
        }

        return system_messages.get(self.use_case, system_messages["it_helpdesk"])

    def _format_chat_history(self) -> List[Dict[str, str]]:
        """Format chat history for function calling."""
        formatted = []
        history = self.conversation_manager.get_history()

        for message in history:
            if hasattr(message, 'content'):
                role = "user" if message.__class__.__name__ == "HumanMessage" else "assistant"
                formatted.append({"role": role, "content": message.content})

        return formatted

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get formatted conversation history."""
        history = []
        messages = self.conversation_manager.get_history()

        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                user_msg = messages[i]
                assistant_msg = messages[i + 1]

                history.append({
                    "user": user_msg.content,
                    "assistant": assistant_msg.content,
                    "timestamp": datetime.now().isoformat()  # Simplified timestamp
                })

        return history

    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_manager.clear_history()
        print("Conversation history cleared.")

    def get_available_functions(self) -> List[str]:
        """Get list of available function names."""
        if self.function_caller:
            return list(self.function_caller.functions.keys())
        return []

    def get_chatbot_stats(self) -> Dict[str, Any]:
        """Get comprehensive chatbot statistics."""
        stats = {
            "use_case": self.use_case,
            "functions_enabled": self.enable_functions,
            "conversation": self.conversation_manager.get_history_summary()
        }

        # Add retrieval chain stats
        stats["retrieval_chain"] = self.retrieval_chain.get_stats()

        # Add function information
        if self.function_caller:
            stats["functions"] = {
                "available_functions": self.get_available_functions(),
                "total_functions": len(self.function_caller.functions)
            }

        return stats

    def demo_interaction(self) -> None:
        """Run a demo interaction showcasing capabilities."""
        print(f"\n=== RAG Chatbot Demo - {self.use_case.title()} ===")

        demo_questions = self._get_demo_questions()

        for i, question in enumerate(demo_questions, 1):
            print(f"\nDemo {i}: {question}")
            print("-" * 50)

            response = self.chat(question)
            print(f"Response: {response['answer']}")

            if response.get('method') == 'function_calling':
                print(f"Method: Function Calling ({response.get('function_calls_made', 0)} calls)")
            elif response.get('method') == 'rag_retrieval':
                print(f"Method: RAG Retrieval")
                if response.get('sources'):
                    print(f"Sources: {', '.join(response['sources'])}")

            print()

    def _get_demo_questions(self) -> List[str]:
        """Get demo questions based on use case."""
        demo_sets = {
            "it_helpdesk": [
                "My computer is running very slowly",
                "What's the status of printer01?",
                "How do I connect to the company VPN?",
                "Can you check if server01 is working?"
            ],
            "customer_support": [
                "How can I track my order?",
                "What's the status of order ORD123456?",
                "Tell me about the wireless headphones",
                "How much is shipping for a $75 order?"
            ],
            "hr_assistant": [
                "How do I request time off?",
                "What's my leave balance for EMP001?",
                "Tell me about health insurance benefits",
                "What company holidays do we have in 2025?"
            ]
        }

        return demo_sets.get(self.use_case, demo_sets["it_helpdesk"])


class ChatInterface:
    """Command-line chat interface for the RAG chatbot."""

    def __init__(self, use_case: str = "it_helpdesk"):
        """Initialize chat interface.

        Args:
            use_case: The use case for the chatbot
        """
        self.chatbot = RAGChatbot(use_case)
        self.use_case = use_case

    def run(self):
        """Run the interactive chat interface."""
        print(f"🤖 Welcome to the {self.use_case.title()} RAG Chatbot!")
        print("Type 'help' for commands, 'quit' to exit, or 'demo' for a demonstration.")
        print("=" * 60)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye! 👋")
                    break

                elif user_input.lower() == 'help':
                    self._show_help()

                elif user_input.lower() == 'demo':
                    self.chatbot.demo_interaction()

                elif user_input.lower() == 'clear':
                    self.chatbot.clear_conversation()

                elif user_input.lower() == 'stats':
                    self._show_stats()

                elif user_input.lower() == 'history':
                    self._show_history()

                else:
                    # Process the message
                    response = self.chatbot.chat(user_input)

                    print(f"\n🤖 Bot: {response['answer']}")

                    # Show additional info if available
                    if response.get('method') == 'function_calling':
                        func_calls = response.get('function_calls_made', 0)
                        if func_calls > 0:
                            print(f"💡 Used {func_calls} function call(s)")

                    elif response.get('sources'):
                        sources = response['sources'][:3]  # Show first 3 sources
                        print(f"📚 Sources: {', '.join(sources)}")

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break

            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    def _show_help(self):
        """Show help information."""
        print("\n📋 Available Commands:")
        print("  help     - Show this help message")
        print("  demo     - Run a demonstration")
        print("  clear    - Clear conversation history")
        print("  stats    - Show chatbot statistics")
        print("  history  - Show conversation history")
        print("  quit     - Exit the chatbot")
        print("\n💬 Just type your question to chat with the bot!")

    def _show_stats(self):
        """Show chatbot statistics."""
        stats = self.chatbot.get_chatbot_stats()
        print("\n📊 Chatbot Statistics:")
        print(f"  Use Case: {stats['use_case']}")
        print(f"  Functions Enabled: {stats['functions_enabled']}")

        if 'functions' in stats:
            print(f"  Available Functions: {stats['functions']['total_functions']}")

        conv_stats = stats['conversation']
        print(f"  Total Messages: {conv_stats['total_messages']}")
        print(f"  User Messages: {conv_stats['user_messages']}")
        print(f"  Bot Messages: {conv_stats['assistant_messages']}")

    def _show_history(self):
        """Show conversation history."""
        history = self.chatbot.get_conversation_history()

        if not history:
            print("\n📝 No conversation history yet.")
            return

        print(f"\n📝 Conversation History ({len(history)} exchanges):")
        print("-" * 50)

        for i, exchange in enumerate(history[-5:], 1):  # Show last 5 exchanges
            print(f"{i}. You: {exchange['user']}")
            print(f"   Bot: {exchange['assistant'][:100]}{'...' if len(exchange['assistant']) > 100 else ''}")
            print()


if __name__ == "__main__":
    # Run command-line interface
    import sys

    use_case = "it_helpdesk"
    if len(sys.argv) > 1:
        use_case = sys.argv[1]

    interface = ChatInterface(use_case)
    interface.run()

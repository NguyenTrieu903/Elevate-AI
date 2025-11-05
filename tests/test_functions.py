"""Tests for function calling functionality."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from rag_system.function_calling import FunctionCaller, FunctionDefinition

class TestFunctionCaller:
    """Test cases for FunctionCaller class."""

    def test_function_caller_initialization(self):
        """Test function caller initialization."""
        fc = FunctionCaller("it_helpdesk")
        assert fc.use_case == "it_helpdesk"
        assert len(fc.functions) > 0
        assert fc.client is not None

    def test_register_function(self):
        """Test function registration."""
        fc = FunctionCaller("it_helpdesk")

        # Register a test function
        def test_func(param1: str) -> str:
            return f"Test result: {param1}"

        fc.register_function(
            name="test_function",
            description="A test function",
            parameters={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "Test parameter"}
                },
                "required": ["param1"]
            },
            handler=test_func
        )

        assert "test_function" in fc.functions
        func_def = fc.functions["test_function"]
        assert func_def.name == "test_function"
        assert func_def.description == "A test function"
        assert callable(func_def.handler)

    def test_get_function_definitions(self):
        """Test getting OpenAI function definitions."""
        fc = FunctionCaller("it_helpdesk")
        definitions = fc.get_function_definitions()

        assert isinstance(definitions, list)
        assert len(definitions) > 0

        # Check structure of first definition
        first_def = definitions[0]
        assert "name" in first_def
        assert "description" in first_def
        assert "parameters" in first_def

    def test_it_helpdesk_functions(self):
        """Test IT helpdesk specific functions."""
        fc = FunctionCaller("it_helpdesk")

        expected_functions = [
            "check_device_status",
            "get_software_info",
            "search_it_solutions"
        ]

        for func_name in expected_functions:
            assert func_name in fc.functions

    def test_customer_support_functions(self):
        """Test customer support specific functions."""
        fc = FunctionCaller("customer_support")

        expected_functions = [
            "check_order_status",
            "get_product_info",
            "calculate_shipping_cost"
        ]

        for func_name in expected_functions:
            assert func_name in fc.functions

    def test_hr_assistant_functions(self):
        """Test HR assistant specific functions."""
        fc = FunctionCaller("hr_assistant")

        expected_functions = [
            "check_leave_balance",
            "get_benefits_information",
            "get_company_holidays",
            "get_training_courses"
        ]

        for func_name in expected_functions:
            assert func_name in fc.functions


class TestFunctionExecution:
    """Test cases for function execution."""

    def test_device_status_function(self):
        """Test device status checking function."""
        fc = FunctionCaller("it_helpdesk")

        # Test with known device
        result = fc.call_function("check_device_status", {"device_id": "printer01"})

        assert isinstance(result, dict)
        assert "device_status" in result or "status" in result

    def test_order_status_function(self):
        """Test order status checking function."""
        fc = FunctionCaller("customer_support")

        # Test with known order
        result = fc.call_function("check_order_status", {"order_id": "ORD123456"})

        assert isinstance(result, dict)
        assert "status" in result

    def test_leave_balance_function(self):
        """Test leave balance checking function."""
        fc = FunctionCaller("hr_assistant")

        # Test with known employee
        result = fc.call_function("check_leave_balance", {"employee_id": "EMP001"})

        assert isinstance(result, dict)
        # Should have employee info or error message
        assert "name" in result or "error" in result

    def test_invalid_function_call(self):
        """Test calling non-existent function."""
        fc = FunctionCaller("it_helpdesk")

        result = fc.call_function("non_existent_function", {})

        assert isinstance(result, dict)
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_function_call_with_invalid_args(self):
        """Test function call with invalid arguments."""
        fc = FunctionCaller("it_helpdesk")

        # Call function without required arguments
        result = fc.call_function("check_device_status", {})

        assert isinstance(result, dict)
        assert "error" in result


class TestMockFunctionCalling:
    """Test function calling with mocked Azure OpenAI client."""

    @patch('rag_system.function_calling.openai.AzureOpenAI')
    def test_chat_with_functions_mock(self, mock_client_class):
        """Test chat with functions using mocked client."""
        # Setup mock response
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_message.function_call = None
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        fc = FunctionCaller("it_helpdesk")

        messages = [
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Test question"}
        ]

        result = fc.chat_with_functions(messages)

        assert "content" in result
        assert result["content"] == "Test response"
        assert result["function_calls_made"] == 0

    @patch('rag_system.function_calling.openai.AzureOpenAI')
    def test_chat_with_function_call_mock(self, mock_client_class):
        """Test chat with actual function call using mocked client."""
        # Setup mock response with function call
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # First response with function call
        mock_function_call = Mock()
        mock_function_call.name = "check_device_status"
        mock_function_call.arguments = '{"device_id": "printer01"}'

        mock_message1 = Mock()
        mock_message1.content = None
        mock_message1.function_call = mock_function_call

        mock_choice1 = Mock()
        mock_choice1.message = mock_message1
        mock_response1 = Mock()
        mock_response1.choices = [mock_choice1]

        # Second response with final answer
        mock_message2 = Mock()
        mock_message2.content = "The printer is online and functioning normally."
        mock_message2.function_call = None

        mock_choice2 = Mock()
        mock_choice2.message = mock_message2
        mock_response2 = Mock()
        mock_response2.choices = [mock_choice2]

        # Setup mock to return different responses on successive calls
        mock_client.chat.completions.create.side_effect = [mock_response1, mock_response2]

        fc = FunctionCaller("it_helpdesk")

        messages = [
            {"role": "user", "content": "What's the status of printer01?"}
        ]

        result = fc.chat_with_functions(messages)

        assert "content" in result
        assert result["function_calls_made"] == 1


class TestFunctionDefinition:
    """Test cases for FunctionDefinition dataclass."""

    def test_function_definition_creation(self):
        """Test creating a function definition."""
        def test_handler(x: int) -> int:
            return x * 2

        func_def = FunctionDefinition(
            name="test_func",
            description="Test function",
            parameters={"type": "object"},
            handler=test_handler
        )

        assert func_def.name == "test_func"
        assert func_def.description == "Test function"
        assert func_def.parameters == {"type": "object"}
        assert func_def.handler == test_handler


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

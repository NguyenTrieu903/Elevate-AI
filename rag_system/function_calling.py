"""Function calling implementation for Azure OpenAI."""

import os
import json
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FunctionDefinition:
    """Function definition for OpenAI function calling."""
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable

class FunctionCaller:
    """Handles Azure OpenAI function calling capabilities."""

    def __init__(self, use_case: str = "it_helpdesk"):
        """Initialize function caller with specified use case.

        Args:
            use_case: The use case for function calling (it_helpdesk, customer_support, hr_assistant)
        """
        self.use_case = use_case
        self.functions: Dict[str, FunctionDefinition] = {}
        self.client = self._initialize_client()

        # Register functions based on use case
        self._register_use_case_functions()

    def _initialize_client(self) -> openai.AzureOpenAI:
        """Initialize Azure OpenAI client."""
        # Use LLM-specific credentials if available, otherwise fallback to general ones
        llm_endpoint = os.getenv("AZURE_OPENAI_LLM_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
        llm_key = os.getenv("AZURE_OPENAI_LLM_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        llm_api_version = os.getenv("AZURE_OPENAI_LLM_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        return openai.AzureOpenAI(
            azure_endpoint=llm_endpoint,
            api_key=llm_key,
            api_version=llm_api_version
        )

    def _register_use_case_functions(self) -> None:
        """Register functions based on the use case."""
        if self.use_case == "it_helpdesk":
            self._register_it_functions()
        elif self.use_case == "customer_support":
            self._register_customer_functions()
        elif self.use_case == "hr_assistant":
            self._register_hr_functions()

    def _register_it_functions(self) -> None:
        """Register IT helpdesk functions."""
        from mock_data.it_helpdesk import get_device_status, get_software_info, search_solutions

        # Device status check function
        self.register_function(
            name="check_device_status",
            description="Check the status of IT devices like printers, servers, routers, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The unique identifier of the device (e.g., printer01, server01)"
                    }
                },
                "required": ["device_id"]
            },
            handler=lambda device_id: self._format_device_status(get_device_status(device_id))
        )

        # Software information function
        self.register_function(
            name="get_software_info",
            description="Get information about available software, licenses, and installation requirements",
            parameters={
                "type": "object",
                "properties": {
                    "software_name": {
                        "type": "string",
                        "description": "Name of the software to look up"
                    }
                },
                "required": ["software_name"]
            },
            handler=lambda software_name: get_software_info(software_name)
        )

        # Troubleshooting search function
        self.register_function(
            name="search_it_solutions",
            description="Search for IT troubleshooting solutions based on keywords",
            parameters={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keywords related to the IT issue"
                    }
                },
                "required": ["keywords"]
            },
            handler=lambda keywords: search_solutions(keywords)
        )

    def _register_customer_functions(self) -> None:
        """Register customer support functions."""
        from mock_data.customer_support import get_order_status, get_product_info, calculate_shipping

        # Order status function
        self.register_function(
            name="check_order_status",
            description="Check the status of a customer order",
            parameters={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to check"
                    }
                },
                "required": ["order_id"]
            },
            handler=lambda order_id: get_order_status(order_id)
        )

        # Product information function
        self.register_function(
            name="get_product_info",
            description="Get information about products including price, availability, and specifications",
            parameters={
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to look up"
                    }
                },
                "required": ["product_name"]
            },
            handler=lambda product_name: get_product_info(product_name)
        )

        # Shipping calculation function
        self.register_function(
            name="calculate_shipping_cost",
            description="Calculate shipping cost based on order total and shipping method",
            parameters={
                "type": "object",
                "properties": {
                    "order_total": {
                        "type": "number",
                        "description": "Total value of the order"
                    },
                    "shipping_type": {
                        "type": "string",
                        "enum": ["standard", "express", "overnight"],
                        "description": "Type of shipping"
                    }
                },
                "required": ["order_total"]
            },
            handler=lambda order_total, shipping_type="standard": calculate_shipping(order_total, shipping_type)
        )

    def _register_hr_functions(self) -> None:
        """Register HR assistant functions."""
        from mock_data.hr_assistant import (
            get_leave_balance, get_benefits_info,
            get_company_holidays, check_holiday_conflict, get_available_training
        )

        # Leave balance function
        self.register_function(
            name="check_leave_balance",
            description="Check employee leave balance (vacation, sick, personal days)",
            parameters={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID (e.g., EMP001)"
                    }
                },
                "required": ["employee_id"]
            },
            handler=lambda employee_id: get_leave_balance(employee_id)
        )

        # Benefits information function
        self.register_function(
            name="get_benefits_information",
            description="Get information about employee benefits",
            parameters={
                "type": "object",
                "properties": {
                    "benefit_type": {
                        "type": "string",
                        "enum": ["health_insurance", "dental_insurance", "vision_insurance", "401k"],
                        "description": "Type of benefit to get information about"
                    }
                }
            },
            handler=lambda benefit_type=None: get_benefits_info(benefit_type)
        )

        # Company holidays function
        self.register_function(
            name="get_company_holidays",
            description="Get list of company holidays for a specific year",
            parameters={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Year to get holidays for"
                    }
                }
            },
            handler=lambda year=2025: get_company_holidays(year)
        )

        # Training courses function
        self.register_function(
            name="get_training_courses",
            description="Get available training courses",
            parameters={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["compliance", "professional", "technical"],
                        "description": "Category of training courses"
                    }
                }
            },
            handler=lambda category=None: get_available_training(category)
        )

    def register_function(self, name: str, description: str, parameters: Dict[str, Any], handler: Callable) -> None:
        """Register a new function for calling.

        Args:
            name: Function name
            description: Function description
            parameters: Function parameters schema
            handler: Function handler callable
        """
        self.functions[name] = FunctionDefinition(
            name=name,
            description=description,
            parameters=parameters,
            handler=handler
        )

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get OpenAI function definitions for API calls."""
        return [
            {
                "name": func.name,
                "description": func.description,
                "parameters": func.parameters
            }
            for func in self.functions.values()
        ]

    def call_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a function call.

        Args:
            function_name: Name of the function to call
            arguments: Function arguments

        Returns:
            Function result
        """
        if function_name not in self.functions:
            return {"error": f"Function '{function_name}' not found"}

        func = self.functions[function_name]

        try:
            # Call the function with unpacked arguments
            result = func.handler(**arguments)
            return result
        except Exception as e:
            return {"error": f"Function execution failed: {str(e)}"}

    def chat_with_functions(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_function_calls: int = 3
    ) -> Dict[str, Any]:
        """Chat with function calling enabled.

        Args:
            messages: Conversation messages
            model: Azure OpenAI model deployment name
            max_function_calls: Maximum number of function calls per response

        Returns:
            Response with function calls if applicable
        """
        if model is None:
            model = os.getenv("AZURE_OPENAI_LLM_MODEL") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "GPT-4o-mini")

        function_calls_made = 0
        current_messages = messages.copy()

        while function_calls_made < max_function_calls:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=current_messages,
                    functions=self.get_function_definitions(),
                    function_call="auto",
                    temperature=0.7
                )

                message = response.choices[0].message

                # Check if function call was made
                if message.function_call:
                    function_calls_made += 1

                    # Execute the function
                    func_name = message.function_call.name
                    func_args = json.loads(message.function_call.arguments)
                    func_result = self.call_function(func_name, func_args)

                    # Add function call and result to messages
                    current_messages.append({
                        "role": "assistant",
                        "content": None,
                        "function_call": {
                            "name": func_name,
                            "arguments": message.function_call.arguments
                        }
                    })
                    current_messages.append({
                        "role": "function",
                        "name": func_name,
                        "content": json.dumps(func_result)
                    })

                    # Continue the conversation
                    continue
                else:
                    # No function call, return the response
                    return {
                        "content": message.content,
                        "function_calls_made": function_calls_made,
                        "messages": current_messages
                    }

            except Exception as e:
                return {
                    "error": f"Chat completion failed: {str(e)}",
                    "function_calls_made": function_calls_made
                }

        return {
            "error": "Maximum function calls reached",
            "function_calls_made": function_calls_made
        }

    def _format_device_status(self, status_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format device status information for better readability."""
        if "status" in status_info:
            return {
                "device_status": status_info["status"],
                "details": status_info.get("details", "No additional details available"),
                "location": status_info.get("location", "Location unknown"),
                "formatted_response": f"Device Status: {status_info['status']}. {status_info.get('details', '')}"
            }
        return status_info


if __name__ == "__main__":
    # Test function calling
    print("Testing Function Calling...")

    # Test IT helpdesk functions
    fc = FunctionCaller("it_helpdesk")

    # Test device status function
    result = fc.call_function("check_device_status", {"device_id": "printer01"})
    print(f"Device Status Result: {result}")

    # Test chat with functions
    messages = [
        {"role": "system", "content": "You are an IT helpdesk assistant."},
        {"role": "user", "content": "What's the status of printer01?"}
    ]

    chat_result = fc.chat_with_functions(messages)
    print(f"Chat Result: {chat_result}")

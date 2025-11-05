"""Run comprehensive tests for the RAG chatbot system."""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests and display results."""
    print("🧪 Running RAG Chatbot System Tests")
    print("=" * 50)

    # Run pytest with verbose output
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-x"  # Stop on first failure
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)

        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with return code {result.returncode}")

        return result.returncode

    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}")
        return 1

def run_specific_test_module(module_name):
    """Run tests from a specific module."""
    print(f"🧪 Running tests from {module_name}")
    print("=" * 50)

    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            f"tests/{module_name}",
            "-v"
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        return result.returncode

    except Exception as e:
        print(f"❌ Error running {module_name}: {str(e)}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test module
        module = sys.argv[1]
        exit_code = run_specific_test_module(module)
    else:
        # Run all tests
        exit_code = run_tests()

    sys.exit(exit_code)

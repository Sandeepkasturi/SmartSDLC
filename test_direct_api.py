#!/usr/bin/env python3
"""
Test script for Watsonx Direct API Integration
This script demonstrates how to use the WatsonxDirectAPI class
"""

import os
import json
from watsonx_direct_api import WatsonxDirectAPI

# Configuration - Replace with your actual credentials
WATSONX_APIKEY = "89B_QQncoXf53DaBc89zWwMpEvJ5lGfUoZ15eJuI7LaA"
WATSONX_PROJECT_ID = "f7f03912-3bc3-43b1-9c1f-bcfb805ec438"
WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

def test_basic_generation():
    """Test basic text generation"""
    print("🧪 Testing Basic Text Generation...")
    
    watsonx = WatsonxDirectAPI(WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, MODEL_ID)
    
    prompt = "Hello! Can you tell me a short joke about programming?"
    response = watsonx.generate_text(prompt)
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print("-" * 50)

def test_code_generation():
    """Test code generation"""
    print("🧪 Testing Code Generation...")
    
    watsonx = WatsonxDirectAPI(WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, MODEL_ID)
    
    requirements = "Create a Python function to calculate the factorial of a number with error handling"
    code = watsonx.generate_code(requirements, "python")
    
    print(f"Requirements: {requirements}")
    print(f"Generated Code:\n{code}")
    print("-" * 50)

def test_bug_fixing():
    """Test bug fixing"""
    print("🧪 Testing Bug Fixing...")
    
    watsonx = WatsonxDirectAPI(WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, MODEL_ID)
    
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # This will fail if numbers is empty
"""
    
    error_desc = "The function fails with ZeroDivisionError when the numbers list is empty"
    fixed_code = watsonx.fix_bugs(buggy_code, error_desc)
    
    print(f"Buggy Code:\n{buggy_code}")
    print(f"Error Description: {error_desc}")
    print(f"Fixed Code:\n{fixed_code}")
    print("-" * 50)

def test_requirements_classification():
    """Test requirements classification"""
    print("🧪 Testing Requirements Classification...")
    
    watsonx = WatsonxDirectAPI(WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, MODEL_ID)
    
    requirements = """
    The system should:
    1. Allow users to register and login
    2. Process payments securely
    3. Handle 1000 concurrent users
    4. Provide real-time notifications
    5. Be accessible on mobile devices
    6. Support multiple languages
    """
    
    classification = watsonx.classify_requirements(requirements)
    
    print(f"Requirements:\n{requirements}")
    print(f"Classification:\n{json.dumps(classification, indent=2)}")
    print("-" * 50)

def test_chat_assistant():
    """Test chat assistant"""
    print("🧪 Testing Chat Assistant...")
    
    watsonx = WatsonxDirectAPI(WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, MODEL_ID)
    
    question = "What are the best practices for writing clean Python code?"
    response = watsonx.chat_assistant(question)
    
    print(f"Question: {question}")
    print(f"Response: {response}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("🚀 Starting Watsonx Direct API Tests")
    print("=" * 60)
    
    try:
        test_basic_generation()
        test_code_generation()
        test_bug_fixing()
        test_requirements_classification()
        test_chat_assistant()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
import requests
import json
import logging
import time
from typing import Dict, Any, Optional

class WatsonxDirectAPI:
    """
    Direct integration with IBM Watsonx API using requests library.
    Provides more control over API parameters and error handling.
    """
    
    def __init__(self, api_key: str, project_id: str, url: str, model_id: str):
        """
        Initialize Watsonx Direct API client.
        
        Args:
            api_key: IBM Cloud API key
            project_id: Watsonx project ID
            url: Watsonx API URL
            model_id: Model ID to use for generation
        """
        self.api_key = api_key
        self.project_id = project_id
        self.url = url.rstrip('/')
        self.model_id = model_id
        self.access_token = None
        self.token_expiry = 0
        
    def _get_access_token(self) -> str:
        """
        Get or refresh the access token for Watsonx API.
        
        Returns:
            Valid access token string
        """
        # Check if we have a valid token
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token
            
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.api_key
            }
            
            response = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                headers=headers,
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data.get("access_token")
            # Set expiry to 50 minutes (tokens typically last 1 hour)
            self.token_expiry = time.time() + 3000
            
            if not self.access_token:
                raise ValueError("No access token received from IBM IAM")
                
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get access token: {e}")
            raise Exception(f"Authentication failed: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse token response: {e}")
            raise Exception("Invalid response from authentication service")
    
    def generate_text(self, prompt: str, type_of_request: str = "general", 
                     max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using Watsonx API.
        
        Args:
            prompt: Input prompt for text generation
            type_of_request: Type of request (affects temperature setting)
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (0.0 to 1.0)
            
        Returns:
            Generated text or error message
        """
        try:
            # Get access token
            access_token = self._get_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Parameters for text generation
            parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "min_new_tokens": 1,
                "stop_sequences": [],
                "temperature": 0.1 if type_of_request == "classify" else temperature,
                "top_k": 50,
                "top_p": 1
            }
            
            payload = {
                "model_id": self.model_id,
                "input": prompt,
                "parameters": parameters,
                "project_id": self.project_id
            }
            
            response = requests.post(
                f"{self.url}/ml/v1-beta/generation/text?version=2023-05-29",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'results' in result and len(result['results']) > 0:
                return result['results'][0]['generated_text']
            else:
                return f"Error: Unexpected response format from Watsonx API: {result}"
                
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"HTTP error occurred: {http_err}"
            if hasattr(http_err, 'response') and http_err.response is not None:
                try:
                    error_detail = http_err.response.json()
                    error_msg += f" - Details: {error_detail}"
                except:
                    error_msg += f" - Response: {http_err.response.text}"
            return error_msg
            
        except requests.exceptions.ConnectionError as conn_err:
            return f"Connection error: {conn_err} - Check network or Watsonx URL: {self.url}"
            
        except requests.exceptions.Timeout as timeout_err:
            return f"Timeout error: {timeout_err} - Watsonx API took too long to respond"
            
        except json.JSONDecodeError as json_err:
            return f"JSON decode error: {json_err} - Could not parse Watsonx API response"
            
        except Exception as e:
            return f"Unexpected error during API call: {str(e)}"
    
    def generate_code(self, requirements: str, language: str = "python") -> str:
        """
        Generate code based on requirements.
        
        Args:
            requirements: Code requirements description
            language: Programming language
            
        Returns:
            Generated code
        """
        prompt = f"""You are an expert software developer. Generate high-quality, production-ready {language} code based on the following requirements.

Requirements: {requirements}

Please provide:
1. Clean, well-documented code
2. Proper error handling
3. Best practices implementation
4. Comments explaining key functionality

Generate only the code with appropriate comments. Do not include explanations outside the code.

Code:"""
        
        return self.generate_text(prompt, type_of_request="code", temperature=0.7)
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """
        Generate test cases for given code.
        
        Args:
            code: Code to generate tests for
            framework: Testing framework to use
            
        Returns:
            Generated test code
        """
        prompt = f"""You are a QA engineer. Generate comprehensive test cases using {framework} for the following code:

Code:
{code}

Generate:
1. Unit tests covering all functions
2. Edge cases and error handling tests
3. Integration tests if applicable
4. Test data and fixtures

Provide only the test code with appropriate imports and setup.

Test Code:"""
        
        return self.generate_text(prompt, type_of_request="test", temperature=0.7)
    
    def fix_bugs(self, code: str, error_description: str) -> str:
        """
        Fix bugs in the provided code.
        
        Args:
            code: Code with bugs
            error_description: Description of the error/issue
            
        Returns:
            Fixed code
        """
        prompt = f"""You are a senior software engineer. Fix the bugs in the following code:

Code with bugs:
{code}

Error/Issue description:
{error_description}

Provide:
1. Fixed code with corrections highlighted in comments
2. Brief explanation of what was wrong
3. Best practices to prevent similar issues

Focus on providing the corrected code with clear comments indicating fixes.

Fixed Code:"""
        
        return self.generate_text(prompt, type_of_request="fix", temperature=0.7)
    
    def summarize_code(self, code: str) -> str:
        """
        Summarize and explain code functionality.
        
        Args:
            code: Code to analyze
            
        Returns:
            Code analysis and summary
        """
        prompt = f"""You are a technical documentation expert. Analyze and summarize the following code:

Code:
{code}

Provide a comprehensive analysis including:
1. High-level summary of functionality
2. Key components and their purposes
3. Input/output description
4. Dependencies and requirements
5. Potential improvements or concerns

Format your response in clear sections with headings.

Analysis:"""
        
        return self.generate_text(prompt, type_of_request="summarize", temperature=0.7)
    
    def classify_requirements(self, requirements: str) -> Dict[str, Any]:
        """
        Classify requirements into categories.
        
        Args:
            requirements: Requirements text to classify
            
        Returns:
            Dictionary with classified requirements
        """
        prompt = f"""You are a business analyst. Classify the following requirements into structured categories:

Requirements:
{requirements}

Analyze and classify into:
1. Functional Requirements
2. Non-functional Requirements
3. Technical Requirements
4. Business Requirements
5. Priority Level (High/Medium/Low)
6. Complexity Estimate (Simple/Medium/Complex)

Format the output as a valid JSON object with these exact keys:
- "Functional Requirements": [list of items]
- "Non-functional Requirements": [list of items]
- "Technical Requirements": [list of items]
- "Business Requirements": [list of items]
- "Priority Level": "High/Medium/Low"
- "Complexity Estimate": "Simple/Medium/Complex"

Respond with only the JSON object, no additional text.

JSON:"""
        
        response = self.generate_text(prompt, type_of_request="classify", temperature=0.1)
        
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "No valid JSON found in response", "raw_response": response}
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse classification response as JSON: {e}")
            return {"error": "Failed to parse classification", "raw_response": response}
        except Exception as e:
            logging.error(f"An error occurred during JSON parsing: {e}")
            return {"error": str(e), "raw_response": response}
    
    def chat_assistant(self, query: str, context: str = "") -> str:
        """
        Conversational assistant for software development.
        
        Args:
            query: User's question
            context: Previous conversation context
            
        Returns:
            AI assistant response
        """
        context_section = f"Context: {context}\n" if context else ""
        
        prompt = f"""You are a helpful AI assistant specialized in software development and programming.

{context_section}

User Query: {query}

Provide a helpful, accurate response that:
1. Directly answers the question
2. Provides code examples if relevant
3. Explains technical concepts clearly
4. Suggests best practices
5. Keeps responses concise and actionable

Response:"""
        
        return self.generate_text(prompt, type_of_request="chat", temperature=0.7)


# Example usage and testing
if __name__ == "__main__":
    # Configuration
    API_KEY = "your_api_key_here"
    PROJECT_ID = "your_project_id_here"
    URL = "https://eu-de.ml.cloud.ibm.com"
    MODEL_ID = "ibm/granite-3-3-8b-instruct"
    
    # Initialize the API client
    watsonx = WatsonxDirectAPI(API_KEY, PROJECT_ID, URL, MODEL_ID)
    
    # Test the API
    test_prompt = "Hello, how are you?"
    response = watsonx.generate_text(test_prompt)
    print(f"Test Response: {response}") 
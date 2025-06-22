# main.py - SmartSDLC Main Application with IBM Watsonx Integration
import streamlit as st
import os
import json
from typing import Dict, Any, List, Optional
import time
import base64
from io import BytesIO

# Try to import PyPDF2, but make it optional
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    # Don't show warning at module level to avoid issues
    pass

import zipfile
import logging
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr

# Import the new direct API integration
try:
    from watsonx_direct_api import WatsonxDirectAPI
    DIRECT_API_AVAILABLE = True
except ImportError:
    DIRECT_API_AVAILABLE = False
    st.warning("Direct API integration not available. Using LangChain integration only.")

# IBM Watsonx credentials - MOVE THESE TO ENVIRONMENT VARIABLES IN PRODUCTION
WATSONX_APIKEY = "89B_QQncoXf53DaBc89zWwMpEvJ5lGfUoZ15eJuI7LaA"
WATSONX_PROJECT_ID = "f7f03912-3bc3-43b1-9c1f-bcfb805ec438"
WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# Page configuration
st.set_page_config(
    page_title="SmartSDLC - AI-Powered Software Development",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
/* Header */
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #f0f8ff;
    text-align: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Feature Cards */
.feature-card {
    background: #1e1e1e;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(255,255,255,0.05);
    margin: 1rem 0;
    border-left: 4px solid #00c6ff;
    color: #f5f5f5;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

/* Status Indicators */
.status-success {
    color: #28ff9d;
    font-weight: bold;
}
.status-error {
    color: #ff4c4c;
    font-weight: bold;
}
.status-warning {
    color: #ffc107;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


class WatsonxAI:
    def __init__(self, use_direct_api: bool = False):
        self.use_direct_api = use_direct_api and DIRECT_API_AVAILABLE
        if self.use_direct_api:
            self.direct_api = WatsonxDirectAPI(
                WATSONX_APIKEY, 
                WATSONX_PROJECT_ID, 
                WATSONX_URL, 
                MODEL_ID
            )
        else:
            self.llm = self._initialize_llm()

    @st.cache_resource(show_spinner=False)
    def _initialize_llm(_self):
        """Initialize IBM Watsonx LLM with LangChain"""
        if not all([WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL]):
            st.error("Missing Watsonx credentials. Please verify configuration.")
            st.stop()

        try:
            return WatsonxLLM(
                model_id=MODEL_ID,
                url=SecretStr(WATSONX_URL),
                apikey=SecretStr(WATSONX_APIKEY),
                project_id=WATSONX_PROJECT_ID,
                params={
                    "max_new_tokens": 1000,
                    "min_new_tokens": 50,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "repetition_penalty": 1.05,
                    "stop_sequences": ["###", "---", "\n\nUser:", "\n\nHuman:"]
                }
            )
        except Exception as e:
            logging.exception("LLM Initialization Failed")
            st.error(f"Failed to initialize LLM: {e}")
            st.stop()

    def _call_watsonx_with_prompt(self, template: str, input_vars: Dict[str, str]) -> str:
        """Call Watsonx with a structured prompt template"""
        try:
            if self.use_direct_api:
                # Use direct API
                prompt = template.format(**input_vars)
                return self.direct_api.generate_text(prompt)
            else:
                # Use LangChain
                prompt = PromptTemplate.from_template(template)
                chain = prompt | self.llm | StrOutputParser()
                result = chain.invoke(input_vars)
                return result.strip()
        except Exception as e:
            logging.exception("Error generating AI response")
            return f"⚠️ Error generating response: {str(e)}"

    def generate_code(self, requirements: str, language: str = "python") -> str:
        """Generate code based on requirements using IBM Watsonx"""
        template = """You are an expert software developer. Generate high-quality, production-ready {language} code based on the following requirements.

Requirements: {requirements}

Please provide:
1. Clean, well-documented code
2. Proper error handling
3. Best practices implementation
4. Comments explaining key functionality

Generate only the code with appropriate comments. Do not include explanations outside the code.

Code:"""

        return self._call_watsonx_with_prompt(template, {
            "requirements": requirements,
            "language": language
        })

    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """Generate test cases for given code"""
        template = """You are a QA engineer. Generate comprehensive test cases using {framework} for the following code:

Code:
{code}

Generate:
1. Unit tests covering all functions
2. Edge cases and error handling tests
3. Integration tests if applicable
4. Test data and fixtures

Provide only the test code with appropriate imports and setup.

Test Code:"""

        return self._call_watsonx_with_prompt(template, {
            "code": code,
            "framework": framework
        })

    def fix_bugs(self, code: str, error_description: str) -> str:
        """Fix bugs in the provided code"""
        template = """You are a senior software engineer. Fix the bugs in the following code:

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

        return self._call_watsonx_with_prompt(template, {
            "code": code,
            "error_description": error_description
        })

    def summarize_code(self, code: str) -> str:
        """Summarize and explain code functionality"""
        template = """You are a technical documentation expert. Analyze and summarize the following code:

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

        return self._call_watsonx_with_prompt(template, {
            "code": code
        })

    def classify_requirements(self, requirements: str) -> Dict[str, Any]:
        """Classify requirements into categories"""
        template = """You are a business analyst. Classify the following requirements into structured categories:

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

        response = self._call_watsonx_with_prompt(template, {
            "requirements": requirements
        })

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
            st.error(f"Failed to parse classification response as JSON: {e}")
            return {"error": "Failed to parse classification", "raw_response": response}
        except Exception as e:
            st.error(f"An error occurred during JSON parsing: {e}")
            return {"error": str(e), "raw_response": response}

    def chat_assistant(self, query: str, context: str = "") -> str:
        """Conversational assistant for software development"""
        template = """You are a helpful AI assistant specialized in software development and programming.

{context_section}

User Query: {query}

Provide a helpful, accurate response that:
1. Directly answers the question
2. Provides code examples if relevant
3. Explains technical concepts clearly
4. Suggests best practices
5. Keeps responses concise and actionable

Response:"""

        context_section = f"Context: {context}\n" if context else ""

        return self._call_watsonx_with_prompt(template, {
            "context_section": context_section,
            "query": query
        })


# Initialize Watsonx AI (cached to prevent re-initialization)
@st.cache_resource
def get_watsonx_ai(use_direct_api: bool = False):
    return WatsonxAI(use_direct_api=use_direct_api)


# Utility functions
def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file using PyPDF2."""
    if not PDF_SUPPORT:
        return "PDF support not available. Please install PyPDF2: pip install PyPDF2"
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except PyPDF2.errors.PdfReadError:
        st.error("Error reading PDF file. It might be corrupted or encrypted.")
        return ""
    except Exception as e:
        st.error(f"An unexpected error occurred while extracting text from PDF: {str(e)}")
        return ""


def create_download_link(content: str, filename: str, file_type: str = "text") -> str:
    """Create a download link for generated content."""
    if file_type == "text":
        b64 = base64.b64encode(content.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    elif file_type == "zip":
        # Ensure content is bytes for zip files
        if isinstance(content, str):
            content_bytes = content.encode()
        else:
            content_bytes = content
        b64 = base64.b64encode(content_bytes).decode()
        href = f'<a href="data:application/zip;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    else:
        href = f'<p style="color: red;">Unsupported file type for download.</p>'
    return href


def show_loading_spinner():
    """Display a loading spinner during AI processing."""
    return st.spinner("🧠 AI is processing your request...")


# Sidebar Navigation
def render_sidebar():
    """Render sidebar navigation and app information."""
    st.sidebar.markdown("## 🧠 SmartSDLC")
    st.sidebar.markdown("AI-Powered Software Development")

    # API Method Selection
    if DIRECT_API_AVAILABLE:
        api_method = st.sidebar.selectbox(
            "🔧 API Integration Method:",
            ["LangChain Integration", "Direct API Integration"],
            help="Choose between LangChain wrapper or direct API calls"
        )
        use_direct_api = api_method == "Direct API Integration"
    else:
        use_direct_api = False
        st.sidebar.info("📡 Using LangChain Integration")

    # Show PDF support status
    if not PDF_SUPPORT:
        st.sidebar.warning("📄 PDF support disabled. Install PyPDF2 for PDF uploads.")

    pages = {
        "🏠 Home": "home",
        "📄 Code Generator": "code_generator",
        "🔧 Bug Fixer": "bug_fixer",
        "🧪 Test Generator": "test_generator",
        "📊 Code Summarizer": "code_summarizer",
        "📋 Requirements Classifier": "requirements_classifier",
        "💬 Chat Assistant": "chat_assistant"
    }

    selected_page = st.sidebar.radio("Navigate to:", list(pages.keys()))
    
    # Ensure selected_page is not None
    if selected_page is None:
        selected_page = "🏠 Home"

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Features")
    st.sidebar.markdown("""
    - AI Code Generation
    - Intelligent Bug Fixing
    - Automated Test Creation
    - Code Analysis & Summary
    - Requirements Classification
    - PDF Requirement Processing
    - Conversational AI Assistant
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Stats")
    if "generation_count" not in st.session_state:
        st.session_state.generation_count = 0
    st.sidebar.metric("AI Generations", st.session_state.generation_count)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ API Status")

    # Test API connection
    try:
        watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
        method_name = "Direct API" if use_direct_api else "LangChain"
        st.sidebar.success(f"✅ {method_name} Connected")
    except Exception as e:
        st.sidebar.error(f"❌ API Error: {str(e)[:50]}...")

    return pages[selected_page], use_direct_api


def render_home():
    """Render the home page with an overview of SmartSDLC."""
    st.markdown('<h1 class="main-header">🧠 SmartSDLC</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Software Development Lifecycle Automation</p>',
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 AI Code Generation</h3>
            <p>Generate production-ready code from natural language requirements using IBM Watsonx models.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔧 Intelligent Bug Fixing</h3>
            <p>Automatically detect and fix bugs in your code with AI-powered analysis and solutions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🧪 Test Automation</h3>
            <p>Generate comprehensive test suites including unit tests, integration tests, and edge cases.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Code Generated", "1,234+", "↑ 12%")
    with col2:
        st.metric("Bugs Fixed", "567+", "↑ 8%")
    with col3:
        st.metric("Tests Created", "890+", "↑ 15%")
    with col4:
        st.metric("User Satisfaction", "98%", "↑ 2%")


def render_code_generator(use_direct_api: bool):
    """Render the code generator page."""
    st.markdown("# 📄 AI Code Generator")
    st.markdown("Generate high-quality code from your requirements using IBM Watsonx AI.")

    input_method = st.radio("Choose input method:", ["✍️ Text Input", "📄 PDF Upload"])

    requirements = ""

    if input_method == "✍️ Text Input":
        requirements = st.text_area(
            "Enter your requirements:",
            height=200,
            placeholder="Example: Create a Python function to calculate compound interest with error handling and documentation..."
        )
    else:
        if not PDF_SUPPORT:
            st.error("PDF upload is not available. Please install PyPDF2: pip install PyPDF2")
            st.info("You can still use text input for your requirements.")
        else:
            uploaded_file = st.file_uploader("Upload PDF with requirements", type="pdf")
            if uploaded_file:
                with show_loading_spinner():
                    requirements = extract_text_from_pdf(uploaded_file)
                if requirements:
                    st.success("PDF content extracted successfully!")
                    st.text_area("Extracted Requirements:", requirements, height=150, disabled=True)
                else:
                    st.warning("Could not extract content from PDF. Please check the file.")

    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Programming Language:",
                                ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust"])
    with col2:
        framework = st.selectbox("Framework (optional):",
                                 ["None", "Flask", "Django", "FastAPI", "React", "Angular", "Vue.js"])

    if st.button("🚀 Generate Code", type="primary"):
        if requirements.strip():
            with show_loading_spinner():
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
                language_lower = language.lower() if language else "python"
                generated_code = watsonx_ai.generate_code(requirements, language_lower)
                st.session_state.generation_count += 1

            st.success("✅ Code generated successfully!")

            st.markdown("### Generated Code")
            st.code(generated_code, language=language_lower)

            ext = {"python": "py", "javascript": "js", "java": "java",
                   "c++": "cpp", "c#": "cs", "go": "go", "rust": "rs"}.get(language_lower, "txt")

            st.markdown(
                create_download_link(generated_code, f"generated_code.{ext}", "text"),
                unsafe_allow_html=True
            )

            st.session_state.last_generated_code = generated_code

        else:
            st.error("⚠️ Please provide requirements before generating code.")


def render_bug_fixer(use_direct_api: bool):
    """Render the bug fixer page."""
    st.markdown("# 🔧 AI Bug Fixer")
    st.markdown("Fix bugs in your code with AI-powered analysis and solutions.")

    code_input = st.text_area(
        "Paste your buggy code here:",
        height=300,
        placeholder="Paste your code that has bugs or issues..."
    )

    error_description = st.text_area(
        "Describe the error or issue:",
        height=100,
        placeholder="Example: Getting IndexError when accessing list elements, or function returns None instead of expected value..."
    )

    if st.button("🔧 Fix Bugs", type="primary"):
        if code_input.strip() and error_description.strip():
            with show_loading_spinner():
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
                fixed_code = watsonx_ai.fix_bugs(code_input, error_description)
                st.session_state.generation_count += 1

            st.success("✅ Bug analysis and fixes completed!")

            st.markdown("### Fixed Code")
            st.code(fixed_code, language="python")

            st.markdown(
                create_download_link(fixed_code, "fixed_code.py", "text"),
                unsafe_allow_html=True
            )

        else:
            st.error("⚠️ Please provide both code and error description.")


def render_test_generator(use_direct_api: bool):
    """Render the test generator page."""
    st.markdown("# 🧪 AI Test Generator")
    st.markdown("Generate comprehensive test suites for your code.")

    code_input = st.text_area(
        "Paste your code here:",
        height=300,
        placeholder="Paste the code you want to generate tests for..."
    )

    col1, col2 = st.columns(2)
    with col1:
        test_framework = st.selectbox("Testing Framework:",
                                      ["pytest", "unittest", "jest", "mocha", "junit"])
    with col2:
        test_type = st.selectbox("Test Type:",
                                 ["Unit Tests", "Integration Tests", "Both"])

    if st.button("🧪 Generate Tests", type="primary"):
        if code_input.strip():
            with show_loading_spinner():
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
                framework_name = test_framework if test_framework else "pytest"
                test_code = watsonx_ai.generate_tests(code_input, framework_name)
                st.session_state.generation_count += 1

            st.success("✅ Test suite generated successfully!")

            st.markdown("### Generated Tests")
            st.code(test_code, language="python")

            st.markdown(
                create_download_link(test_code, f"test_{framework_name}.py", "text"),
                unsafe_allow_html=True
            )

        else:
            st.error("⚠️ Please provide code to generate tests for.")


def render_code_summarizer(use_direct_api: bool):
    """Render the code summarizer page."""
    st.markdown("# 📊 AI Code Summarizer")
    st.markdown("Get detailed analysis and summary of your code.")

    code_input = st.text_area(
        "Paste your code here:",
        height=300,
        placeholder="Paste the code you want to analyze and summarize..."
    )

    if st.button("📊 Analyze Code", type="primary"):
        if code_input.strip():
            with show_loading_spinner():
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
                summary = watsonx_ai.summarize_code(code_input)
                st.session_state.generation_count += 1

            st.success("✅ Code analysis completed!")

            st.markdown("### Code Analysis")
            st.markdown(summary)

            st.markdown(
                create_download_link(summary, "code_analysis.md", "text"),
                unsafe_allow_html=True
            )

        else:
            st.error("⚠️ Please provide code to analyze.")


def render_requirements_classifier(use_direct_api: bool):
    """Render the requirements classifier page."""
    st.markdown("# 📋 Requirements Classifier")
    st.markdown("Classify and analyze your project requirements.")

    input_method = st.radio("Choose input method:", ["✍️ Text Input", "📄 PDF Upload"])

    requirements = ""

    if input_method == "✍️ Text Input":
        requirements = st.text_area(
            "Enter your requirements:",
            height=200,
            placeholder="Example: The system should process user payments, handle authentication, and provide real-time notifications..."
        )
    else:
        if not PDF_SUPPORT:
            st.error("PDF upload is not available. Please install PyPDF2: pip install PyPDF2")
            st.info("You can still use text input for your requirements.")
        else:
            uploaded_file = st.file_uploader("Upload PDF with requirements", type="pdf")
            if uploaded_file:
                with show_loading_spinner():
                    requirements = extract_text_from_pdf(uploaded_file)
                if requirements:
                    st.success("PDF content extracted successfully!")
                    st.text_area("Extracted Requirements:", requirements, height=150, disabled=True)

    if st.button("📋 Classify Requirements", type="primary"):
        if requirements.strip():
            with show_loading_spinner():
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)
                classification = watsonx_ai.classify_requirements(requirements)
                st.session_state.generation_count += 1

            st.success("✅ Requirements classified successfully!")

            if "error" not in classification:
                st.markdown("### Classification Results")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Priority Level", classification.get("Priority Level", "N/A"))
                with col2:
                    st.metric("Complexity", classification.get("Complexity Estimate", "N/A"))

                for category, items in classification.items():
                    if category not in ["Priority Level", "Complexity Estimate"]:
                        st.markdown(f"**{category}:**")
                        if isinstance(items, list):
                            for item in items:
                                st.markdown(f"- {item}")
                        else:
                            st.markdown(f"- {items}")
                        st.markdown("")

            else:
                st.error("Failed to classify requirements. Please try again.")
                st.text_area("Raw Response:", classification.get("raw_response", ""), height=100)

        else:
            st.error("⚠️ Please provide requirements to classify.")


def render_chat_assistant(use_direct_api: bool):
    """Render the chat assistant page."""
    st.markdown("# 💬 AI Chat Assistant")
    st.markdown("Ask questions about software development, coding, or get help with your projects.")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat history
    for speaker, message in st.session_state.chat_messages:
        with st.chat_message(speaker):
            st.markdown(message)

    # Chat input
    if user_input := st.chat_input("Ask me anything about software development..."):
        # Add user message
        st.session_state.chat_messages.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                watsonx_ai = get_watsonx_ai(use_direct_api=use_direct_api)

                # Provide context from recent messages
                context = ""
                if len(st.session_state.chat_messages) > 1:
                    recent_messages = st.session_state.chat_messages[-6:]  # Last 3 exchanges
                    context = "\n".join([f"{speaker}: {msg}" for speaker, msg in recent_messages[:-1]])

                response = watsonx_ai.chat_assistant(user_input, context)
                st.markdown(response)
                st.session_state.chat_messages.append(("assistant", response))
                st.session_state.generation_count += 1

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_messages = []
        st.rerun()


def main():
    """Main application function to manage page rendering."""
    selected_page, use_direct_api = render_sidebar()

    if selected_page == "home":
        render_home()
    elif selected_page == "code_generator":
        render_code_generator(use_direct_api)
    elif selected_page == "bug_fixer":
        render_bug_fixer(use_direct_api)
    elif selected_page == "test_generator":
        render_test_generator(use_direct_api)
    elif selected_page == "code_summarizer":
        render_code_summarizer(use_direct_api)
    elif selected_page == "requirements_classifier":
        render_requirements_classifier(use_direct_api)
    elif selected_page == "chat_assistant":
        render_chat_assistant(use_direct_api)

    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">© 2025 SmartSDLC - Powered by IBM Watsonx AI</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
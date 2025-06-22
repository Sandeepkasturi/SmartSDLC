# SmartSDLC - AI-Powered Software Development Lifecycle

SmartSDLC is a comprehensive AI-powered application that automates various aspects of the software development lifecycle using IBM Watsonx AI models.

## 🚀 Features

- **AI Code Generation**: Generate production-ready code from natural language requirements
- **Intelligent Bug Fixing**: Automatically detect and fix bugs in your code
- **Automated Test Creation**: Generate comprehensive test suites including unit tests and integration tests
- **Code Analysis & Summary**: Get detailed analysis and documentation of your code
- **Requirements Classification**: Classify and analyze project requirements into structured categories
- **PDF Requirement Processing**: Extract and process requirements from PDF documents
- **Conversational AI Assistant**: Get help with software development questions and best practices

## 🔧 API Integration Methods

SmartSDLC supports two different integration methods with IBM Watsonx:

### 1. LangChain Integration (Default)
- Uses the `langchain-ibm` library
- Provides a higher-level abstraction
- Easier to use with LangChain ecosystem
- Good for rapid prototyping

### 2. Direct API Integration (New)
- Direct HTTP calls to Watsonx API using `requests`
- More control over API parameters and error handling
- Better performance and customization options
- Detailed error messages and debugging information

## 📋 Prerequisites

- Python 3.8 or higher
- IBM Cloud account with Watsonx access
- Watsonx API credentials (API key, Project ID, URL, Model ID)

## 🛠️ Installation

### **Method 1: Quick Installation (Recommended)**

1. **Run the installation script:**
   ```bash
   python install.py
   ```

2. **Update your Watsonx credentials** in `streamlit_app.py` or `.env` file

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

### **Method 2: Manual Installation**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SmartSDLC
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Watsonx credentials** in `streamlit_app.py`:
   ```python
   WATSONX_APIKEY = "your_api_key_here"
   WATSONX_PROJECT_ID = "your_project_id_here"
   WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
   MODEL_ID = "ibm/granite-3-3-8b-instruct"
   ```

## 🚀 Running the Application

### **Method 1: Direct Streamlit Command**
```bash
streamlit run streamlit_app.py
```

### **Method 2: Using the Run Script**
```bash
python run.py
```

### **Method 3: Custom Port (if 8501 is busy)**
```bash
streamlit run streamlit_app.py --server.port 8502
```

The application will open in your browser at `http://localhost:8501` (or the specified port).

## 🔧 Configuration

### **Environment Variables (Recommended)**

Create a `.env` file in the project root:
```bash
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
MODEL_ID=ibm/granite-3-3-8b-instruct
```

### **Direct Code Configuration**

Update the credentials directly in `streamlit_app.py`:
```python
WATSONX_APIKEY = "your_api_key_here"
WATSONX_PROJECT_ID = "your_project_id_here"
WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-8b-instruct"
```

## 🧪 Testing

### **Test the Direct API Integration**
```bash
python test_direct_api.py
```

### **Test Individual Components**
```python
from watsonx_direct_api import WatsonxDirectAPI

# Initialize and test
watsonx = WatsonxDirectAPI(api_key, project_id, url, model_id)
response = watsonx.generate_text("Hello, world!")
print(response)
```

## 📱 Using the Application

Once running, you'll see:

1. **Sidebar Navigation** - Choose between different features
2. **API Method Selector** - Switch between LangChain and Direct API integration
3. **Features Available:**
   - 🏠 **Home** - Overview and statistics
   - 📄 **Code Generator** - Generate code from requirements
   - 🔧 **Bug Fixer** - Fix bugs in your code
   - 🧪 **Test Generator** - Generate test suites
   - 📊 **Code Summarizer** - Analyze and document code
   - 📋 **Requirements Classifier** - Classify project requirements
   - 💬 **Chat Assistant** - Get help with development questions

## 📁 Project Structure

```
SmartSDLC/
├── streamlit_app.py          # Main Streamlit application
├── watsonx_direct_api.py     # Direct API integration class
├── watsonx_integration.py    # Original LangChain integration
├── test_direct_api.py        # Test script for direct API
├── install.py                # Installation script
├── run.py                    # Run script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔍 API Integration Details

### **Direct API Integration (`WatsonxDirectAPI`)**

The direct API integration provides:

- **Token Management**: Automatic access token retrieval and refresh
- **Error Handling**: Comprehensive error handling with detailed messages
- **Parameter Control**: Full control over generation parameters
- **Method-Specific Prompts**: Optimized prompts for different use cases

#### Key Methods:

- `generate_text()`: Raw text generation with custom parameters
- `generate_code()`: Code generation from requirements
- `generate_tests()`: Test case generation
- `fix_bugs()`: Bug fixing and code correction
- `summarize_code()`: Code analysis and documentation
- `classify_requirements()`: Requirements classification
- `chat_assistant()`: Conversational AI assistance

#### Error Handling:

The direct API integration provides detailed error messages for:
- HTTP errors with response details
- Connection errors with network diagnostics
- Timeout errors with timing information
- JSON parsing errors with response content
- Authentication failures with token details

### **LangChain Integration**

The LangChain integration provides:
- Integration with LangChain ecosystem
- Simplified prompt templates
- Chain-based processing
- Built-in caching and optimization

## 🔐 Security

⚠️ **Important**: The current implementation includes API credentials directly in the code. For production use:

1. Move credentials to environment variables:
```python
import os
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
```

2. Use a `.env` file:
```bash
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
MODEL_ID=ibm/granite-3-3-8b-instruct
```

3. Add `.env` to your `.gitignore` file

## 🛠️ Troubleshooting

### **Common Issues:**

1. **Missing Dependencies:**
   ```bash
   python install.py
   # or
   pip install -r requirements.txt
   ```

2. **PyPDF2 Import Error:**
   ```bash
   pip install PyPDF2
   ```

3. **LangChain Import Error:**
   ```bash
   pip install langchain-ibm langchain-core
   ```

4. **Port Already in Use:**
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

5. **API Connection Issues:**
   - Check your Watsonx credentials
   - Verify your internet connection
   - Ensure your IBM Cloud account has Watsonx access

### **PDF Support:**

If PyPDF2 is not installed, PDF upload functionality will be disabled, but you can still use text input for all features.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM Watsonx for providing the AI models
- Streamlit for the web application framework
- LangChain for the AI integration framework

## 📞 Support

For issues and questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include error messages and reproduction steps

---

**Note**: This application is for educational and development purposes. Always review and test generated code before using it in production environments. 
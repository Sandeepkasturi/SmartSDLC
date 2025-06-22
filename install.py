#!/usr/bin/env python3
"""
Installation script for SmartSDLC
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "streamlit>=1.28.0",
        "langchain-ibm>=0.0.1", 
        "langchain-core>=0.1.0",
        "requests>=2.31.0",
        "PyPDF2>=3.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0"
    ]
    
    failed_packages = []
    for package in packages:
        print(f"   Installing {package}...")
        if install_package(package):
            print(f"   ✅ {package}")
        else:
            print(f"   ❌ {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Failed to install: {', '.join(failed_packages)}")
        print("   You can try installing them manually:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed successfully!")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "streamlit",
        "langchain_ibm",
        "langchain_core", 
        "requests",
        "PyPDF2",
        "pydantic"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("\n✅ All dependencies are available!")
    return True

def create_env_file():
    """Create a .env file template"""
    env_content = """# IBM Watsonx Credentials
# Replace these with your actual credentials
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
MODEL_ID=ibm/granite-3-3-8b-instruct
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("   Please update it with your actual Watsonx credentials")
    else:
        print("ℹ️ .env file already exists")

def main():
    """Main installation function"""
    print("🚀 SmartSDLC Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    print()
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️ Warning: You're not in a virtual environment.")
        print("   It's recommended to create one first:")
        print("   python -m venv .venv")
        print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
        print()
    
    # Install requirements
    if not install_requirements():
        return
    
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print()
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your Watsonx credentials in streamlit_app.py or .env file")
    print("2. Run the application: streamlit run streamlit_app.py")
    print("3. Or use the run script: python run.py")
    print("4. Open your browser to http://localhost:8501")
    print("\n🔧 For testing the direct API: python test_direct_api.py")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Deployment script for SmartSDLC
Handles environment variables and credentials for different deployment platforms
"""

import os
import json
from pathlib import Path

def create_streamlit_secrets():
    """Create Streamlit secrets.toml for deployment"""
    secrets_content = """# Streamlit secrets.toml
# This file contains sensitive configuration for deployment
# DO NOT commit this file to version control

[watsonx]
api_key = "your_api_key_here"
project_id = "your_project_id_here"
url = "https://eu-de.ml.cloud.ibm.com"
model_id = "ibm/granite-3-3-8b-instruct"
"""
    
    secrets_file = Path(".streamlit/secrets.toml")
    secrets_file.parent.mkdir(exist_ok=True)
    
    if not secrets_file.exists():
        with open(secrets_file, "w") as f:
            f.write(secrets_content)
        print("✅ Created .streamlit/secrets.toml")
        print("   Please update it with your actual Watsonx credentials")
    else:
        print("ℹ️ .streamlit/secrets.toml already exists")

def update_app_for_deployment():
    """Update the app to use environment variables for deployment"""
    
    # Read current app content
    with open("streamlit_app.py", "r") as f:
        content = f.read()
    
    # Replace hardcoded credentials with environment variables
    updated_content = content.replace(
        'WATSONX_APIKEY = "89B_QQncoXf53DaBc89zWwMpEvJ5lGfUoZ15eJuI7LaA"',
        'WATSONX_APIKEY = st.secrets.get("watsonx", {}).get("api_key", os.getenv("WATSONX_APIKEY", ""))'
    )
    
    updated_content = updated_content.replace(
        'WATSONX_PROJECT_ID = "f7f03912-3bc3-43b1-9c1f-bcfb805ec438"',
        'WATSONX_PROJECT_ID = st.secrets.get("watsonx", {}).get("project_id", os.getenv("WATSONX_PROJECT_ID", ""))'
    )
    
    updated_content = updated_content.replace(
        'WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"',
        'WATSONX_URL = st.secrets.get("watsonx", {}).get("url", os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com"))'
    )
    
    updated_content = updated_content.replace(
        'MODEL_ID = "ibm/granite-3-3-8b-instruct"',
        'MODEL_ID = st.secrets.get("watsonx", {}).get("model_id", os.getenv("MODEL_ID", "ibm/granite-3-3-8b-instruct"))'
    )
    
    # Write updated content
    with open("streamlit_app_deploy.py", "w") as f:
        f.write(updated_content)
    
    print("✅ Created streamlit_app_deploy.py with environment variable support")

def create_dockerfile():
    """Create Dockerfile for container deployment"""
    dockerfile_content = """# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the application
CMD ["streamlit", "run", "streamlit_app_deploy.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Created Dockerfile for container deployment")

def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    compose_content = """version: '3.8'

services:
  smartsdlc:
    build: .
    ports:
      - "8501:8501"
    environment:
      - WATSONX_APIKEY=${WATSONX_APIKEY}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - WATSONX_URL=${WATSONX_URL}
      - MODEL_ID=${MODEL_ID}
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("✅ Created docker-compose.yml")

def create_heroku_files():
    """Create files for Heroku deployment"""
    
    # Procfile for Heroku
    procfile_content = """web: streamlit run streamlit_app_deploy.py --server.port=$PORT --server.address=0.0.0.0
"""
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # runtime.txt for Heroku
    runtime_content = """python-3.9.18
"""
    
    with open("runtime.txt", "w") as f:
        f.write(runtime_content)
    
    print("✅ Created Heroku deployment files (Procfile, runtime.txt)")

def create_vercel_config():
    """Create Vercel configuration"""
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "streamlit_app_deploy.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "streamlit_app_deploy.py"
            }
        ]
    }
    
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created vercel.json for Vercel deployment")

def main():
    """Main deployment setup function"""
    print("🚀 SmartSDLC Deployment Setup")
    print("=" * 40)
    
    # Create deployment files
    create_streamlit_secrets()
    update_app_for_deployment()
    create_dockerfile()
    create_docker_compose()
    create_heroku_files()
    create_vercel_config()
    
    print("\n🎉 Deployment files created successfully!")
    print("\n📋 Deployment Instructions:")
    print("\n1. **Streamlit Cloud (Recommended):**")
    print("   - Push code to GitHub")
    print("   - Go to https://share.streamlit.io/")
    print("   - Connect your repository")
    print("   - Add secrets in the dashboard")
    print("   - Deploy!")
    
    print("\n2. **Docker Deployment:**")
    print("   docker build -t smartsdlc .")
    print("   docker run -p 8501:8501 -e WATSONX_APIKEY=your_key smartsdlc")
    
    print("\n3. **Docker Compose:**")
    print("   docker-compose up -d")
    
    print("\n4. **Heroku:**")
    print("   heroku create your-app-name")
    print("   heroku config:set WATSONX_APIKEY=your_key")
    print("   git push heroku main")
    
    print("\n5. **Vercel:**")
    print("   vercel --prod")
    
    print("\n⚠️  Remember to:")
    print("   - Update credentials in .streamlit/secrets.toml")
    print("   - Set environment variables in your deployment platform")
    print("   - Never commit credentials to version control")

if __name__ == "__main__":
    main() 
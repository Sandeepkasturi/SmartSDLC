#!/usr/bin/env python3
"""
Quick Deployment Script for SmartSDLC
Guides you through the deployment process
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git():
    """Check if git is available and repository is initialized"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is available")
            return True
        else:
            print("❌ Git is not available")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False

def check_git_repo():
    """Check if current directory is a git repository"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            return True
        else:
            print("❌ Not a git repository")
            return False
    except:
        return False

def init_git_repo():
    """Initialize git repository if not already done"""
    if not check_git_repo():
        print("📁 Initializing git repository...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial SmartSDLC commit'])
        print("✅ Git repository initialized")

def check_credentials():
    """Check if credentials are properly configured"""
    secrets_file = Path(".streamlit/secrets.toml")
    if secrets_file.exists():
        with open(secrets_file, 'r') as f:
            content = f.read()
            if "your_api_key_here" in content:
                print("⚠️  Please update your credentials in .streamlit/secrets.toml")
                return False
            else:
                print("✅ Credentials configured")
                return True
    else:
        print("❌ .streamlit/secrets.toml not found")
        return False

def deploy_streamlit_cloud():
    """Guide through Streamlit Cloud deployment"""
    print("\n🌐 Streamlit Cloud Deployment")
    print("=" * 40)
    
    if not check_git():
        print("Please install Git first: https://git-scm.com/")
        return
    
    init_git_repo()
    
    # Check if remote exists
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("\n📋 Steps to deploy:")
        print("1. Create a GitHub repository")
        print("2. Add remote origin:")
        print("   git remote add origin https://github.com/yourusername/your-repo.git")
        print("3. Push to GitHub:")
        print("   git push -u origin main")
        print("4. Go to https://share.streamlit.io/")
        print("5. Connect your GitHub repository")
        print("6. Set main file path: streamlit_app.py")
        print("7. Add secrets in the dashboard")
        print("8. Deploy!")
    else:
        print("✅ Remote origin found")
        print("Push to GitHub: git push origin main")
        print("Then deploy at: https://share.streamlit.io/")

def deploy_docker():
    """Guide through Docker deployment"""
    print("\n🐳 Docker Deployment")
    print("=" * 40)
    
    # Check if Docker is available
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
        else:
            print("❌ Docker is not available")
            print("Install Docker: https://docs.docker.com/get-docker/")
            return
    except FileNotFoundError:
        print("❌ Docker is not installed")
        print("Install Docker: https://docs.docker.com/get-docker/")
        return
    
    print("\n📋 Docker deployment commands:")
    print("1. Build the image:")
    print("   docker build -t smartsdlc .")
    print("\n2. Run with environment variables:")
    print("   docker run -d \\")
    print("     -p 8501:8501 \\")
    print("     -e WATSONX_APIKEY=\"your_api_key\" \\")
    print("     -e WATSONX_PROJECT_ID=\"your_project_id\" \\")
    print("     -e WATSONX_URL=\"https://eu-de.ml.cloud.ibm.com\" \\")
    print("     -e MODEL_ID=\"ibm/granite-3-3-8b-instruct\" \\")
    print("     --name smartsdlc-app \\")
    print("     smartsdlc")
    print("\n3. Access at: http://localhost:8501")

def deploy_heroku():
    """Guide through Heroku deployment"""
    print("\n🚀 Heroku Deployment")
    print("=" * 40)
    
    # Check if Heroku CLI is available
    try:
        result = subprocess.run(['heroku', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Heroku CLI is available")
        else:
            print("❌ Heroku CLI is not available")
            print("Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
            return
    except FileNotFoundError:
        print("❌ Heroku CLI is not installed")
        print("Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    print("\n📋 Heroku deployment commands:")
    print("1. Login to Heroku:")
    print("   heroku login")
    print("\n2. Create Heroku app:")
    print("   heroku create your-smartsdlc-app")
    print("\n3. Set environment variables:")
    print("   heroku config:set WATSONX_APIKEY=\"your_api_key\"")
    print("   heroku config:set WATSONX_PROJECT_ID=\"your_project_id\"")
    print("   heroku config:set WATSONX_URL=\"https://eu-de.ml.cloud.ibm.com\"")
    print("   heroku config:set MODEL_ID=\"ibm/granite-3-3-8b-instruct\"")
    print("\n4. Deploy:")
    print("   git push heroku main")
    print("\n5. Open the app:")
    print("   heroku open")

def main():
    """Main deployment guide"""
    print("🚀 SmartSDLC Quick Deployment Guide")
    print("=" * 50)
    
    # Check credentials
    if not check_credentials():
        print("\n⚠️  Please configure your credentials first:")
        print("1. Update .streamlit/secrets.toml with your Watsonx credentials")
        print("2. Run this script again")
        return
    
    print("\n📋 Choose your deployment method:")
    print("1. Streamlit Cloud (Recommended - Free)")
    print("2. Docker (Full control)")
    print("3. Heroku (Easy cloud deployment)")
    print("4. View all options (DEPLOYMENT.md)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        deploy_streamlit_cloud()
    elif choice == "2":
        deploy_docker()
    elif choice == "3":
        deploy_heroku()
    elif choice == "4":
        print("\n📖 View DEPLOYMENT.md for all deployment options")
        print("   Includes: Railway, Vercel, Google Cloud Run, AWS, etc.")
    else:
        print("❌ Invalid choice")
    
    print("\n🎉 Happy deploying!")
    print("📚 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 
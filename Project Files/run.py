#!/usr/bin/env python3
"""
Run script for SmartSDLC
"""

import subprocess
import sys
import os

def main():
    """Run the SmartSDLC application"""
    print("🚀 Starting SmartSDLC...")
    print("=" * 30)
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit is not installed. Please run:")
        print("pip install -r requirements.txt")
        return
    
    # Check if the main app file exists
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found in current directory")
        return
    
    print("🌐 Starting Streamlit server...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 30)
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 SmartSDLC stopped by user")
    except Exception as e:
        print(f"❌ Error running SmartSDLC: {e}")

if __name__ == "__main__":
    main() 
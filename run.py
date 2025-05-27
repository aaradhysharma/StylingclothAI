#!/usr/bin/env python3
"""
Startup script for the Outfit Color Matcher application.
Allows choosing between Flask and FastAPI implementations.
"""

import sys
import subprocess
import os

def print_banner():
    """Print application banner"""
    print("🎨" + "=" * 58 + "🎨")
    print("🎨" + " " * 58 + "🎨")
    print("🎨" + "    OUTFIT COLOR MATCHER - STARTUP SCRIPT    ".center(58) + "🎨")
    print("🎨" + " " * 58 + "🎨")
    print("🎨" + "=" * 58 + "🎨")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import fastapi
        import PIL
        import sklearn
        import numpy
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: pip install -r requirements.txt")
        return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running test suite...")
    try:
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_flask_app():
    """Start the Flask application"""
    print("🚀 Starting Flask application...")
    print("📍 URL: http://127.0.0.1:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Flask application stopped.")

def start_fastapi_app():
    """Start the FastAPI application"""
    print("🚀 Starting FastAPI application...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "fastapi_app.py"])
    except KeyboardInterrupt:
        print("\n👋 FastAPI application stopped.")

def show_menu():
    """Show the main menu"""
    print("🎯 Choose an option:")
    print()
    print("1. 🌶️  Start Flask App (Simple web interface)")
    print("2. ⚡ Start FastAPI App (API with auto-docs)")
    print("3. 🧪 Run Tests Only")
    print("4. 📊 Show System Info")
    print("5. ❌ Exit")
    print()

def show_system_info():
    """Show system information"""
    print("📊 System Information")
    print("-" * 30)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Platform: {sys.platform}")
    
    # Check file existence
    files_to_check = [
        "app.py", "fastapi_app.py", "color_utils.py", 
        "test_app.py", "requirements.txt"
    ]
    
    print("\n📁 Project files:")
    for file in files_to_check:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"   {status} {file}")
    
    print()

def main():
    """Main application entry point"""
    print_banner()
    
    # Check dependencies first
    if not check_dependencies():
        print("\n💡 Install dependencies and try again.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n" + "="*50)
                start_flask_app()
                print("\n" + "="*50)
                
            elif choice == "2":
                print("\n" + "="*50)
                start_fastapi_app()
                print("\n" + "="*50)
                
            elif choice == "3":
                print("\n" + "="*50)
                run_tests()
                print("\n" + "="*50)
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                print("\n" + "="*50)
                show_system_info()
                input("Press Enter to continue...")
                
            elif choice == "5":
                print("\n👋 Goodbye! Thanks for using Outfit Color Matcher!")
                break
                
            else:
                print("\n❌ Invalid choice. Please enter 1-5.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Outfit Color Matcher!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 
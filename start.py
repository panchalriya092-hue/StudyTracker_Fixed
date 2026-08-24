"""
Study Tracker - Easy Startup Script
Helps you get started quickly
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def print_header():
    print("\n" + "="*60)
    print("     📚 STUDY TRACKER PRO - STARTUP SCRIPT")
    print("="*60 + "\n")

def check_dependencies():
    """Check if required packages are installed"""
    required = ['streamlit', 'numpy', 'pandas', 'matplotlib']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    print_header()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstalling missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing + ["--break-system-packages"])
        print("✅ Dependencies installed!\n")
    else:
        print("✅ All dependencies installed!\n")
    
    # Show menu
    print("Choose an option:")
    print("1. Run demo (creates sample data)")
    print("2. Start app with sample data")
    print("3. Start app from scratch")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🎮 Running demo...")
        subprocess.run([sys.executable, "demo.py"])
        
        print("\n✅ Demo completed!")
        print("\nNow run option 2 to start the app with sample data.")
        
    elif choice == "2":
        print("\n🚀 Starting Streamlit app...")
        
        # Check if data file exists
        if not os.path.exists("study_data.json"):
            print("⚠️  No data file found. Running demo first...")
            subprocess.run([sys.executable, "demo.py"])
        
        print("\n🌐 Opening app in browser...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    elif choice == "3":
        print("\n🚀 Starting fresh Streamlit app...")
        
        # Remove old data if exists
        if os.path.exists("study_data.json"):
            response = input("Delete existing data? (y/n): ").strip().lower()
            if response == 'y':
                os.remove("study_data.json")
                print("✅ Old data removed!")
        
        print("\n🌐 Opening app in browser...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    elif choice == "4":
        print("\n👋 Goodbye!")
        
    else:
        print("\n❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")

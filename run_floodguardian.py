#!/usr/bin/env python3
"""
FloodGuardian AI - Quick Start Script

This script helps you run the FloodGuardian AI system with proper setup checks.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
NPM_CMD = 'npm.cmd' if os.name == 'nt' else 'npm'

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_env_file():
    """Check if .env file exists and is configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: python setup_api_keys.py")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    # Check for placeholder values
    placeholders = [
        'your-project-id.supabase.co',
        'your-service-role-key-here',
        'your-account-sid-here',
        'your-auth-token-here'
    ]
    
    for placeholder in placeholders:
        if placeholder in content:
            print(f"❌ .env file contains placeholder values")
            print("   Run: python setup_api_keys.py")
            return False
    
    print("✅ .env file configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import supabase
        import twilio
        print("✅ Backend dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_node():
    """Check if Node.js is available for frontend"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Node.js not found - frontend will not be available")
    return False

def run_backend():
    """Start the FastAPI backend"""
    print("\n🚀 Starting FloodGuardian AI Backend...")
    
    try:
        # Run the backend
        subprocess.run(
            [
                sys.executable, '-m', 'uvicorn',
                'main:app',
                '--host', '0.0.0.0',
                '--port', '8000',
                '--reload'
            ],
            cwd=str(PROJECT_ROOT / 'backend')
        )
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")

def run_frontend():
    """Start the React frontend (if Node.js is available)"""
    if not (PROJECT_ROOT / 'frontend' / 'package.json').exists():
        print("❌ Frontend not found")
        return False
    
    print("\n🎨 Starting React Frontend...")
    
    try:
        # Install dependencies if needed
        if not (PROJECT_ROOT / 'frontend' / 'node_modules').exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run([NPM_CMD, 'install'], check=True, cwd=str(PROJECT_ROOT / 'frontend'))
        
        # Start the frontend
        subprocess.run([NPM_CMD, 'start'], cwd=str(PROJECT_ROOT / 'frontend'))
    except subprocess.CalledProcessError:
        print("❌ Failed to start frontend")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    
    return True

def run_database_setup():
    """Run database setup if needed"""
    print("\n💾 Setting up database...")
    try:
        subprocess.run([sys.executable, 'setup_database.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Database setup failed")
        return False

def main():
    print("🛡️  FloodGuardian AI - Quick Start")
    print("=" * 40)
    
    # Pre-flight checks
    print("🔍 Running pre-flight checks...")
    
    if not check_python_version():
        return
    
    if not check_env_file():
        return
    
    if not check_dependencies():
        return
    
    node_available = check_node()
    
    print("\n✅ All checks passed!")
    
    # Setup database
    setup_db = input("\n🗄️  Set up database? (y/n): ").strip().lower()
    if setup_db == 'y':
        if not run_database_setup():
            return
    
    # Choose what to run
    print("\n🚀 What would you like to run?")
    print("1. Backend only")
    print("2. Frontend only (requires Node.js)")
    print("3. Both (recommended)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        run_backend()
    elif choice == '2' and node_available:
        run_frontend()
    elif choice == '3':
        print("\n🔄 Starting both services...")
        print("Backend will start first, then frontend in a new terminal")
        print("Press Ctrl+C to stop the backend")
        
        # Start backend
        try:
            import threading
            backend_thread = threading.Thread(target=run_backend)
            backend_thread.daemon = True
            backend_thread.start()
            
            time.sleep(3)  # Give backend time to start
            
            if node_available:
                run_frontend()
            else:
                print("Frontend not available - only backend running")
                backend_thread.join()
                
        except KeyboardInterrupt:
            print("\n🛑 All services stopped")
    else:
        print("❌ Invalid choice or Node.js not available")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your setup and try again.")

"""Main entry point for the salary calculator application."""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def run_backend():
    """Start the FastAPI backend server."""
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    print("🚀 Starting FastAPI backend on http://localhost:8000")
    print("📖 API documentation will be available at http://localhost:8000/docs")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed to start: {e}")


def run_frontend():
    """Start the Streamlit frontend server."""
    frontend_path = Path(__file__).parent / "frontend"
    
    print("🎨 Starting Streamlit frontend on http://localhost:8501")
    print("⚠️  Make sure the backend is running on port 8000 first!")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", 
            str(frontend_path / "streamlit_app.py"),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed to start: {e}")


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(description="IT Salary Calculator - FastAPI + Streamlit")
    parser.add_argument(
        "component", 
        choices=["backend", "frontend", "help"], 
        nargs="?", 
        default="help",
        help="Component to run: backend (FastAPI), frontend (Streamlit), or help"
    )
    
    args = parser.parse_args()
    
    if args.component == "backend":
        run_backend()
    elif args.component == "frontend":
        run_frontend()
    else:
        print("💰 IT Salary Calculator")
        print("=" * 50)
        print("Usage:")
        print("  python main.py backend   - Start FastAPI backend server")
        print("  python main.py frontend  - Start Streamlit frontend")
        print("")
        print("Development workflow:")
        print("1. Start backend:  python main.py backend")
        print("2. Start frontend: python main.py frontend")
        print("3. Open browser:   http://localhost:8501")
        print("")
        print("API documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    main()

@echo off
echo ===================================================
echo              Starting BoardRoom AI
echo ===================================================

if not exist .env (
    echo [INFO] Creating .env file from .env.example...
    copy .env.example .env
)

echo [INFO] Activating virtual environment...
if not exist .venv (
    echo [ERROR] Virtual environment not found. Please run 'uv venv' and install requirements.
    exit /b 1
)

echo [INFO] Starting FastAPI Backend on http://localhost:8000...
start cmd /k ".venv\Scripts\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

echo [INFO] Starting Streamlit Frontend on http://localhost:8501...
.venv\Scripts\streamlit run frontend/app.py --server.port 8501

pause

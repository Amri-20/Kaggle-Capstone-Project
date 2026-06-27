import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "boardroom_ai_secret_key_1234567890_super_secure")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./boardroom.db")

# Static folders for files
REPORTS_DIR = os.getenv("REPORTS_DIR", "backend/static/reports")
CHARTS_DIR = os.getenv("CHARTS_DIR", "backend/static/charts")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "backend/static/uploads")

# Create directories if they don't exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

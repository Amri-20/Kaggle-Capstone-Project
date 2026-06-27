import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database.models import init_db
from backend.api.routes import router

# Initialize SQLite database
init_db()

app = FastAPI(
    title="BoardRoom AI API",
    description="Backend API for the BoardRoom AI Multi-Agent business decision platform.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folders mapping
static_dir = "backend/static"
os.makedirs(static_dir, exist_ok=True)
os.makedirs(f"{static_dir}/reports", exist_ok=True)
os.makedirs(f"{static_dir}/charts", exist_ok=True)
os.makedirs(f"{static_dir}/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register API Router
app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "BoardRoom AI API",
        "timestamp": os.getenv("CURRENT_TIME", "2026-06-26T19:00:00")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import engine, Base
from app.routes import upload, analyze, report, auth, user

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="GeM Bid Analyzer API - Automated Tender vs Bid Technical Compliance & Comparison",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/user", tags=["User Dashboard"])
app.include_router(upload.router, prefix=settings.API_V1_STR, tags=["Upload"])
app.include_router(analyze.router, prefix=settings.API_V1_STR, tags=["Analysis"])
app.include_router(report.router, prefix=settings.API_V1_STR, tags=["Report"])

# Static files directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Welcome to GeM Bid Analyzer API",
        "docs": "/docs",
        "health": "OK"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

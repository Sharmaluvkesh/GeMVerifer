import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "GeM Bid Analyzer"
    API_V1_STR: str = "/api"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./gem_analyzer.db")
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "./uploaded_files"))

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

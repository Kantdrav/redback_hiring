import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads" / "resumes"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/instance/interviewflow.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB uploads
    ALLOWED_EXTENSIONS = {"pdf"}

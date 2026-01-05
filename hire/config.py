import os
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads" / "resumes"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    
    # Priority: DATABASE_URL (Render Postgres) > explicit MySQL > SQLite
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Render uses postgres://... but SQLAlchemy needs postgresql://...
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to explicit MySQL env vars (for local development)
        MYSQL_USER = os.environ.get("MYSQL_USER")
        MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
        MYSQL_HOST = os.environ.get("MYSQL_HOST")
        MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
        MYSQL_DB = os.environ.get("MYSQL_DB")

        if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DB:
            # URL-encode password to handle special characters like @, !, etc.
            encoded_password = quote_plus(MYSQL_PASSWORD)
            SQLALCHEMY_DATABASE_URI = (
                f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
            )
        else:
            # Final fallback: SQLite for local development
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/instance/interviewflow.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB uploads
    ALLOWED_EXTENSIONS = {"pdf"}

"""Application configuration loaded exclusively from environment variables."""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")
load_dotenv(BACKEND_DIR / ".env", override=False)


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = _bool(os.getenv("FLASK_DEBUG"), ENV != "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BACKEND_DIR / 'instance' / 'seamless.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    AUTO_CREATE_DB = _bool(os.getenv("AUTO_CREATE_DB"), True)
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "innolearn")
    MONGODB_AUTH_COLLECTION = os.getenv("MONGODB_AUTH_COLLECTION", "users")
    MONGODB_TIMEOUT_MS = int(os.getenv("MONGODB_TIMEOUT_MS", "5000"))

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(10 * 1024 * 1024)))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BACKEND_DIR / "uploads"))

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "together").lower()
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.together.xyz/v1")
    RAG_MODEL_NAME = os.getenv("RAG_MODEL_NAME", "meta-llama/Llama-3.2-3B-Instruct")
    EMBEDDING_MODEL_NAME = os.getenv(
        "EMBEDDING_MODEL_NAME", "Alibaba-NLP/gte-base-en-v1.5"
    )
    ABSTRACTIVE_MODEL_NAME = os.getenv(
        "ABSTRACTIVE_MODEL_NAME", "facebook/bart-large-cnn"
    )

    ATS_WEIGHTS = {
        "skill_match": float(os.getenv("ATS_WEIGHT_SKILL", "0.40")),
        "keyword_match": float(os.getenv("ATS_WEIGHT_KEYWORD", "0.20")),
        "semantic": float(os.getenv("ATS_WEIGHT_SEMANTIC", "0.25")),
        "experience": float(os.getenv("ATS_WEIGHT_EXPERIENCE", "0.08")),
        "education": float(os.getenv("ATS_WEIGHT_EDUCATION", "0.07")),
    }

    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain",
        "application/octet-stream",
    }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt"
    SECRET_KEY = "test-secret"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    ADMIN_EMAIL = "seed-admin@example.com"
    ADMIN_PASSWORD = ""

from sqlalchemy import text
from flask import Blueprint

from app.extensions import db
from app.utils.error_handlers import success

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    db_ok = True
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    status = 200 if db_ok else 503
    return success({"status": "ok" if db_ok else "degraded", "database": db_ok}, status=status)

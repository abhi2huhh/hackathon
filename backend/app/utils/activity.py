from app.models.activity_log import ActivityLog
from app.extensions import db


def log_activity(user_id: int | None, action: str, detail: str | None = None) -> None:
    db.session.add(ActivityLog(user_id=user_id, action=action, detail=detail))

from datetime import datetime, timezone

from app.extensions import db


class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    __table_args__ = (
        db.UniqueConstraint("user_id", "resource_id", name="uq_user_resource_bookmark"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

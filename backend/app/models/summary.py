from datetime import datetime, timezone

from app.extensions import db


class Summary(db.Model):
    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    source_title = db.Column(db.String(255), nullable=True)
    original_length = db.Column(db.Integer, nullable=False)
    summary_length = db.Column(db.Integer, nullable=False)
    line_count = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(40), nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_title": self.source_title,
            "original_length": self.original_length,
            "summary_length": self.summary_length,
            "line_count": self.line_count,
            "method": self.method,
            "summary": self.summary_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from datetime import datetime, timezone

from app.extensions import db


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.String(40), nullable=False)
    resource_type = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    thumbnail = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    bookmarks = db.relationship("Bookmark", backref="resource", lazy="dynamic")

    def to_dict(self, bookmarked: bool | None = None) -> dict:
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "resource_type": self.resource_type,
            "url": self.url,
            "thumbnail": self.thumbnail,
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if bookmarked is not None:
            data["bookmarked"] = bookmarked
        return data

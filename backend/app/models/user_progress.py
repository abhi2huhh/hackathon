from datetime import datetime, timezone

from app.extensions import db


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    __table_args__ = (
        db.UniqueConstraint("user_id", "roadmap_id", "step_id", name="uq_user_roadmap_step"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmaps.id"), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey("roadmap_steps.id"), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    percent = db.Column(db.Float, default=0)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "roadmap_id": self.roadmap_id,
            "step_id": self.step_id,
            "completed": self.completed,
            "percent": self.percent,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

from datetime import datetime, timezone

from app.extensions import db


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    parsed = db.Column(db.JSON, nullable=True)
    raw_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    analyses = db.relationship("ResumeAnalysis", backref="resume", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_filename": self.original_filename,
            "parsed": self.parsed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_role_id = db.Column(db.Integer, db.ForeignKey("job_roles.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    result = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        payload = dict(self.result or {})
        payload.update(
            {
                "id": self.id,
                "resume_id": self.resume_id,
                "job_role_id": self.job_role_id,
                "score": self.score,
                "created_at": self.created_at.isoformat() if self.created_at else None,
            }
        )
        return payload

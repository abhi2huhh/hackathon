from datetime import datetime, timezone

from app.extensions import db


class JobRole(db.Model):
    __tablename__ = "job_roles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON, nullable=False, default=list)
    preferred_skills = db.Column(db.JSON, nullable=False, default=list)
    keywords = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    analyses = db.relationship("ResumeAnalysis", backref="job_role", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "required_skills": self.required_skills or [],
            "preferred_skills": self.preferred_skills or [],
            "keywords": self.keywords or [],
        }

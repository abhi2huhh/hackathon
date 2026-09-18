from datetime import datetime, timezone

from app.extensions import db


class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(40), nullable=False)
    estimated_duration = db.Column(db.String(80), nullable=False)
    prerequisites = db.Column(db.JSON, nullable=False, default=list)
    skills = db.Column(db.JSON, nullable=False, default=list)
    technologies = db.Column(db.JSON, nullable=False, default=list)
    certifications = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    steps = db.relationship(
        "RoadmapStep",
        backref="roadmap",
        lazy="joined",
        order_by="RoadmapStep.order_index",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_steps: bool = True) -> dict:
        data = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "estimated_duration": self.estimated_duration,
            "prerequisites": self.prerequisites or [],
            "skills": self.skills or [],
            "technologies": self.technologies or [],
            "certifications": self.certifications or [],
            "step_count": len(self.steps or []),
        }
        if include_steps:
            data["steps"] = [step.to_dict() for step in self.steps]
        return data

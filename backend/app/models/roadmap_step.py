from app.extensions import db


class RoadmapStep(db.Model):
    __tablename__ = "roadmap_steps"

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmaps.id"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    stage = db.Column(db.String(40), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.JSON, nullable=False, default=list)
    resources = db.Column(db.JSON, nullable=False, default=list)
    projects = db.Column(db.JSON, nullable=False, default=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "stage": self.stage,
            "order_index": self.order_index,
            "description": self.description,
            "skills": self.skills or [],
            "resources": self.resources or [],
            "projects": self.projects or [],
        }

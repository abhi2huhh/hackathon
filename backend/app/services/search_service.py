from app.models.document import Document
from app.models.job_role import JobRole
from app.models.resource import Resource
from app.models.roadmap import Roadmap


def global_search(term: str, user_id: int | None = None, limit: int = 8) -> dict:
    like = f"%{term}%"
    roadmaps = Roadmap.query.filter(
        Roadmap.title.ilike(like) | Roadmap.description.ilike(like)
    ).limit(limit).all()
    resources = Resource.query.filter(
        Resource.title.ilike(like) | Resource.description.ilike(like)
    ).limit(limit).all()
    roles = JobRole.query.filter(
        JobRole.title.ilike(like) | JobRole.description.ilike(like)
    ).limit(limit).all()
    documents = []
    if user_id:
        documents = (
            Document.query.filter(Document.user_id == user_id, Document.title.ilike(like))
            .limit(limit)
            .all()
        )
    return {
        "roadmaps": [r.to_dict(include_steps=False) for r in roadmaps],
        "resources": [r.to_dict() for r in resources],
        "job_roles": [r.to_dict() for r in roles],
        "documents": [d.to_dict() for d in documents],
    }

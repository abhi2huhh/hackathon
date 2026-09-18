from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.document import Document
from app.models.job_role import JobRole
from app.models.resource import Resource
from app.models.roadmap import Roadmap
from app.models.roadmap_step import RoadmapStep
from app.models.user import User
from app.services.mongo_auth_service import sync_role
from app.utils.error_handlers import APIError, success
from app.utils.security import admin_required
from app.utils.validators import require_fields

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/stats")
@jwt_required()
@admin_required
def stats():
    return success(
        {
            "users": User.query.count(),
            "job_roles": JobRole.query.count(),
            "roadmaps": Roadmap.query.count(),
            "resources": Resource.query.count(),
            "documents": Document.query.count(),
        }
    )


@admin_bp.get("/users")
@jwt_required()
@admin_required
def users():
    items = User.query.order_by(User.created_at.desc()).all()
    return success([u.to_dict() for u in items])


@admin_bp.patch("/users/<int:user_id>")
@jwt_required()
@admin_required
def update_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        raise APIError("NOT_FOUND", "User was not found.", 404)
    payload = request.get_json(silent=True) or {}
    if "role" in payload:
        if payload["role"] not in {"USER", "ADMIN"}:
            raise APIError("VALIDATION_ERROR", "role must be USER or ADMIN.", 400)
        user.role = payload["role"]
        sync_role(user)
    db.session.commit()
    return success(user.to_dict(), "User updated.")


@admin_bp.post("/job-roles")
@jwt_required()
@admin_required
def create_role():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, ["title", "description"])
    role = JobRole(
        title=payload["title"].strip(),
        description=payload["description"].strip(),
        required_skills=payload.get("required_skills") or [],
        preferred_skills=payload.get("preferred_skills") or [],
        keywords=payload.get("keywords") or [],
    )
    db.session.add(role)
    db.session.commit()
    return success(role.to_dict(), "Job role created.", 201)


@admin_bp.put("/job-roles/<int:role_id>")
@jwt_required()
@admin_required
def update_role(role_id: int):
    role = JobRole.query.get(role_id)
    if not role:
        raise APIError("NOT_FOUND", "Job role was not found.", 404)
    payload = request.get_json(silent=True) or {}
    for field in ("title", "description", "required_skills", "preferred_skills", "keywords"):
        if field in payload:
            setattr(role, field, payload[field])
    db.session.commit()
    return success(role.to_dict(), "Job role updated.")


@admin_bp.delete("/job-roles/<int:role_id>")
@jwt_required()
@admin_required
def delete_role(role_id: int):
    role = JobRole.query.get(role_id)
    if not role:
        raise APIError("NOT_FOUND", "Job role was not found.", 404)
    db.session.delete(role)
    db.session.commit()
    return success({}, "Job role deleted.")


@admin_bp.post("/resources")
@jwt_required()
@admin_required
def create_resource():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, ["title", "description", "category", "subject", "difficulty", "resource_type", "url"])
    item = Resource(
        title=payload["title"],
        description=payload["description"],
        category=payload["category"],
        subject=payload["subject"],
        difficulty=payload["difficulty"],
        resource_type=payload["resource_type"].upper(),
        url=payload["url"],
        thumbnail=payload.get("thumbnail"),
        tags=payload.get("tags") or [],
    )
    db.session.add(item)
    db.session.commit()
    return success(item.to_dict(), "Resource created.", 201)


@admin_bp.put("/resources/<int:resource_id>")
@jwt_required()
@admin_required
def update_resource(resource_id: int):
    item = Resource.query.get(resource_id)
    if not item:
        raise APIError("NOT_FOUND", "Resource was not found.", 404)
    payload = request.get_json(silent=True) or {}
    for field in ("title", "description", "category", "subject", "difficulty", "resource_type", "url", "thumbnail", "tags"):
        if field in payload:
            setattr(item, field, payload[field])
    db.session.commit()
    return success(item.to_dict(), "Resource updated.")


@admin_bp.delete("/resources/<int:resource_id>")
@jwt_required()
@admin_required
def delete_resource(resource_id: int):
    item = Resource.query.get(resource_id)
    if not item:
        raise APIError("NOT_FOUND", "Resource was not found.", 404)
    db.session.delete(item)
    db.session.commit()
    return success({}, "Resource deleted.")


@admin_bp.post("/roadmaps")
@jwt_required()
@admin_required
def create_roadmap():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, ["title", "slug", "description", "difficulty", "estimated_duration"])
    roadmap = Roadmap(
        title=payload["title"],
        slug=payload["slug"],
        description=payload["description"],
        difficulty=payload["difficulty"],
        estimated_duration=payload["estimated_duration"],
        prerequisites=payload.get("prerequisites") or [],
        skills=payload.get("skills") or [],
        technologies=payload.get("technologies") or [],
        certifications=payload.get("certifications") or [],
    )
    db.session.add(roadmap)
    db.session.flush()
    for index, step in enumerate(payload.get("steps") or []):
        db.session.add(
            RoadmapStep(
                roadmap_id=roadmap.id,
                title=step.get("title", f"Step {index + 1}"),
                stage=step.get("stage", "BEGINNER"),
                order_index=step.get("order_index", index),
                description=step.get("description", ""),
                skills=step.get("skills") or [],
                resources=step.get("resources") or [],
                projects=step.get("projects") or [],
            )
        )
    db.session.commit()
    return success(roadmap.to_dict(), "Roadmap created.", 201)

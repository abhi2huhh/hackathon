from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.roadmap import Roadmap
from app.services.roadmap_service import progress_for_user, set_step_progress
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success

roadmaps_bp = Blueprint("roadmaps", __name__)


@roadmaps_bp.get("")
@jwt_required()
def list_roadmaps():
    items = Roadmap.query.order_by(Roadmap.title.asc()).all()
    return success([item.to_dict(include_steps=False) for item in items])


@roadmaps_bp.get("/<int:roadmap_id>")
@jwt_required()
def detail(roadmap_id: int):
    item = Roadmap.query.get(roadmap_id)
    if not item:
        raise APIError("NOT_FOUND", "Roadmap was not found.", 404)
    user_id = int(get_jwt_identity())
    data = item.to_dict()
    data["progress"] = progress_for_user(user_id, item)
    return success(data)


@roadmaps_bp.post("/<int:roadmap_id>/progress")
@jwt_required()
def progress(roadmap_id: int):
    item = Roadmap.query.get(roadmap_id)
    if not item:
        raise APIError("NOT_FOUND", "Roadmap was not found.", 404)
    payload = request.get_json(silent=True) or {}
    step_id = payload.get("step_id")
    completed = bool(payload.get("completed", True))
    if not step_id:
        raise APIError("VALIDATION_ERROR", "step_id is required.", 400)
    user_id = int(get_jwt_identity())
    summary = set_step_progress(user_id, item, int(step_id), completed)
    log_activity(user_id, "roadmap_progress", item.title)
    db.session.commit()
    return success(summary, "Progress updated.")

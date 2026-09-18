from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.bookmark import Bookmark
from app.models.resource import Resource
from app.services.resource_service import list_resources, toggle_bookmark
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success
from app.utils.validators import clamp_int

resources_bp = Blueprint("resources", __name__)


@resources_bp.get("")
@jwt_required()
def list_all():
    page = clamp_int(request.args.get("page", 1), 1, 1000, "page")
    per_page = clamp_int(request.args.get("per_page", 12), 1, 50, "per_page")
    items, total = list_resources(
        subject=request.args.get("subject"),
        difficulty=request.args.get("difficulty"),
        resource_type=request.args.get("type"),
        tag=request.args.get("tag"),
        q=request.args.get("q"),
        page=page,
        per_page=per_page,
    )
    user_id = int(get_jwt_identity())
    bookmarked_ids = {
        b.resource_id for b in Bookmark.query.filter_by(user_id=user_id).all()
    }
    return success(
        {
            "items": [item.to_dict(bookmarked=item.id in bookmarked_ids) for item in items],
            "total": total,
            "page": page,
            "per_page": per_page,
        }
    )


@resources_bp.get("/bookmarks")
@jwt_required()
def bookmarks():
    user_id = int(get_jwt_identity())
    rows = Bookmark.query.filter_by(user_id=user_id).all()
    ids = [r.resource_id for r in rows]
    items = Resource.query.filter(Resource.id.in_(ids)).all() if ids else []
    return success([item.to_dict(bookmarked=True) for item in items])


@resources_bp.get("/<int:resource_id>")
@jwt_required()
def detail(resource_id: int):
    item = Resource.query.get(resource_id)
    if not item:
        raise APIError("NOT_FOUND", "Resource was not found.", 404)
    user_id = int(get_jwt_identity())
    marked = Bookmark.query.filter_by(user_id=user_id, resource_id=item.id).first() is not None
    return success(item.to_dict(bookmarked=marked))


@resources_bp.post("/<int:resource_id>/bookmark")
@jwt_required()
def bookmark(resource_id: int):
    item = Resource.query.get(resource_id)
    if not item:
        raise APIError("NOT_FOUND", "Resource was not found.", 404)
    user_id = int(get_jwt_identity())
    marked = toggle_bookmark(user_id, resource_id)
    log_activity(user_id, "bookmark" if marked else "unbookmark", item.title)
    db.session.commit()
    return success({"bookmarked": marked}, "Bookmark updated.")

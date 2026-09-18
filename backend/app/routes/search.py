from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.search_service import global_search
from app.utils.error_handlers import APIError, success
from app.utils.validators import sanitize_query

search_bp = Blueprint("search", __name__)


@search_bp.get("")
@jwt_required()
def search():
    term = sanitize_query(request.args.get("q", ""))
    if len(term) < 2:
        raise APIError("VALIDATION_ERROR", "Enter at least 2 characters to search.", 400)
    user_id = int(get_jwt_identity())
    return success(global_search(term, user_id=user_id))

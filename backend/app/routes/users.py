from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.activity_log import ActivityLog
from app.models.bookmark import Bookmark
from app.models.document import Document
from app.models.resource import Resource
from app.models.resume import ResumeAnalysis
from app.models.roadmap import Roadmap
from app.models.summary import Summary
from app.models.user import User
from app.models.user_progress import UserProgress
from app.services.roadmap_service import progress_for_user
from app.utils.error_handlers import APIError, success

users_bp = Blueprint("users", __name__)


@users_bp.get("/me/dashboard")
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        raise APIError("UNAUTHORIZED", "User no longer exists.", 401)

    analyses = (
        ResumeAnalysis.query.filter_by(user_id=user_id)
        .order_by(ResumeAnalysis.created_at.desc())
        .limit(5)
        .all()
    )
    documents = user.documents.order_by(Document.created_at.desc()).limit(5).all()
    summaries = user.summaries.order_by(Summary.created_at.desc()).limit(5).all()
    bookmark_rows = Bookmark.query.filter_by(user_id=user_id).all()
    resource_ids = [b.resource_id for b in bookmark_rows]
    bookmarks = Resource.query.filter(Resource.id.in_(resource_ids)).all() if resource_ids else []
    activities = (
        ActivityLog.query.filter_by(user_id=user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(8)
        .all()
    )
    progress_rows = UserProgress.query.filter_by(user_id=user_id).all()
    roadmap_ids = {row.roadmap_id for row in progress_rows}
    roadmaps = Roadmap.query.filter(Roadmap.id.in_(roadmap_ids)).all() if roadmap_ids else []
    progress = [
        {"roadmap": rm.to_dict(include_steps=False), **progress_for_user(user_id, rm)}
        for rm in roadmaps
    ]
    recommended = Roadmap.query.limit(3).all()
    return success(
        {
            "user": user.to_dict(),
            "ats_analyses": [a.to_dict() for a in analyses],
            "documents": [d.to_dict() for d in documents],
            "summaries": [s.to_dict() for s in summaries],
            "bookmarks": [b.to_dict(bookmarked=True) for b in bookmarks],
            "activity": [a.to_dict() for a in activities],
            "roadmap_progress": progress,
            "recommended_roadmaps": [r.to_dict(include_steps=False) for r in recommended],
        }
    )

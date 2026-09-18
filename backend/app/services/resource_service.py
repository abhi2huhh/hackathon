from app.models.bookmark import Bookmark
from app.models.resource import Resource
from app.extensions import db


def list_resources(subject=None, difficulty=None, resource_type=None, tag=None, q=None, page=1, per_page=12):
    query = Resource.query
    if subject:
        query = query.filter(Resource.subject.ilike(subject))
    if difficulty:
        query = query.filter(Resource.difficulty.ilike(difficulty))
    if resource_type:
        query = query.filter(Resource.resource_type.ilike(resource_type))
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Resource.title.ilike(like), Resource.description.ilike(like)))
    items = query.order_by(Resource.created_at.desc()).all()
    if tag:
        tag_l = tag.lower()
        items = [item for item in items if any(tag_l == (t or "").lower() for t in (item.tags or []))]
    total = len(items)
    start = (page - 1) * per_page
    return items[start : start + per_page], total


def toggle_bookmark(user_id: int, resource_id: int) -> bool:
    existing = Bookmark.query.filter_by(user_id=user_id, resource_id=resource_id).first()
    if existing:
        db.session.delete(existing)
        return False
    db.session.add(Bookmark(user_id=user_id, resource_id=resource_id))
    return True

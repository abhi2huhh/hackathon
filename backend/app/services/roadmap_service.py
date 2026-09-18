from app.models.roadmap import Roadmap
from app.models.user_progress import UserProgress
from app.extensions import db


def progress_for_user(user_id: int, roadmap: Roadmap) -> dict:
    total = len(roadmap.steps or [])
    rows = UserProgress.query.filter_by(user_id=user_id, roadmap_id=roadmap.id).all()
    completed_ids = {row.step_id for row in rows if row.completed and row.step_id}
    percent = round((len(completed_ids) / total) * 100, 1) if total else 0
    return {
        "completed_step_ids": list(completed_ids),
        "percent": percent,
        "completed_count": len(completed_ids),
        "total_steps": total,
    }


def set_step_progress(user_id: int, roadmap: Roadmap, step_id: int, completed: bool) -> dict:
    step_ids = {step.id for step in roadmap.steps}
    if step_id not in step_ids:
        from app.utils.error_handlers import APIError

        raise APIError("VALIDATION_ERROR", "Step does not belong to this roadmap.", 400)
    row = UserProgress.query.filter_by(user_id=user_id, roadmap_id=roadmap.id, step_id=step_id).first()
    if row is None:
        row = UserProgress(user_id=user_id, roadmap_id=roadmap.id, step_id=step_id)
        db.session.add(row)
    row.completed = completed
    summary = progress_for_user(user_id, roadmap)
    row.percent = summary["percent"]
    return summary

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.job_role import JobRole
from app.models.resume import Resume, ResumeAnalysis
from app.services.ats_service import analyze_resume
from app.services.resume_parser import parse_resume
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success
from app.utils.file_utils import save_upload

ats_bp = Blueprint("ats", __name__)


@ats_bp.get("/roles")
@jwt_required()
def roles():
    items = JobRole.query.order_by(JobRole.title.asc()).all()
    return success([role.to_dict() for role in items])


@ats_bp.post("/analyze")
@jwt_required()
def analyze():
    user_id = int(get_jwt_identity())
    role_id = request.form.get("job_role_id") or (request.get_json(silent=True) or {}).get("job_role_id")
    if not role_id:
        raise APIError("VALIDATION_ERROR", "job_role_id is required.", 400)
    role = JobRole.query.get(role_id)
    if not role:
        raise APIError("NOT_FOUND", "Job role was not found.", 404)
    file = request.files.get("file")
    original, stored, path = save_upload(file, {"pdf", "docx"})
    parsed = parse_resume(path, original)
    result = analyze_resume(parsed, role.to_dict(), current_app.config["ATS_WEIGHTS"])
    resume = Resume(
        user_id=user_id,
        original_filename=original,
        stored_filename=stored,
        parsed={k: v for k, v in parsed.items() if k != "raw_text"},
        raw_text=parsed.get("raw_text"),
    )
    db.session.add(resume)
    db.session.flush()
    analysis = ResumeAnalysis(
        user_id=user_id,
        resume_id=resume.id,
        job_role_id=role.id,
        score=result["score"],
        result={**result, "role": role.to_dict()},
    )
    db.session.add(analysis)
    log_activity(user_id, "ats_analyze", role.title)
    db.session.commit()
    return success(analysis.to_dict(), "Estimated compatibility score generated.")


@ats_bp.get("/history")
@jwt_required()
def history():
    user_id = int(get_jwt_identity())
    rows = (
        ResumeAnalysis.query.filter_by(user_id=user_id)
        .order_by(ResumeAnalysis.created_at.desc())
        .all()
    )
    return success([row.to_dict() for row in rows])

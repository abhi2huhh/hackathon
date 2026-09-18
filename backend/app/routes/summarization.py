from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.summary import Summary
from app.services.resume_parser import extract_text
from app.services.summarization_service import summarize
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success
from app.utils.file_utils import save_upload
from app.utils.validators import clamp_int

summarization_bp = Blueprint("summarization", __name__)


def _run(user_id: int, text: str, line_count: int, method: str, title: str | None):
    result = summarize(text, line_count, method)
    record = Summary(
        user_id=user_id,
        source_title=title,
        original_length=result["original_length"],
        summary_length=result["summary_length"],
        line_count=result["line_count"],
        method=result["method"],
        summary_text=result["summary"],
    )
    db.session.add(record)
    log_activity(user_id, "summarize", result["method"])
    db.session.commit()
    return {**result, "id": record.id}


@summarization_bp.post("")
@jwt_required()
def summarize_text():
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        raise APIError("VALIDATION_ERROR", "text is required.", 400)
    if len(text) > 60000:
        raise APIError("VALIDATION_ERROR", "Text exceeds the 60,000 character limit.", 400)
    line_count = clamp_int(payload.get("line_count", 5), 3, 20, "line_count")
    method = payload.get("method", "extractive")
    data = _run(user_id, text, line_count, method, payload.get("title"))
    return success(data, "Summary generated.")


@summarization_bp.post("/document")
@jwt_required()
def summarize_document():
    user_id = int(get_jwt_identity())
    line_count = clamp_int(request.form.get("line_count", 5), 3, 20, "line_count")
    method = request.form.get("method", "extractive")
    original, stored, path = save_upload(request.files.get("file"), {"pdf", "docx", "txt"})
    text = extract_text(path, original)
    data = _run(user_id, text, line_count, method, original)
    return success(data, "Document summarized.")

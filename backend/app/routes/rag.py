from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.document import Document
from app.services.rag_service import ingest_document, query_document
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success
from app.utils.file_utils import save_upload

rag_bp = Blueprint("rag", __name__)


@rag_bp.get("/documents")
@jwt_required()
def list_documents():
    user_id = int(get_jwt_identity())
    docs = Document.query.filter_by(user_id=user_id).order_by(Document.created_at.desc()).all()
    return success([d.to_dict() for d in docs])


@rag_bp.post("/upload")
@jwt_required()
def upload():
    user_id = int(get_jwt_identity())
    original, stored, path = save_upload(request.files.get("file"), {"pdf", "docx", "txt"})
    title = request.form.get("title") or original
    document = ingest_document(user_id, title, original, stored, path, original.rsplit(".", 1)[-1].lower())
    log_activity(user_id, "rag_upload", title)
    db.session.commit()
    return success(document.to_dict(), "Document indexed for question answering.", 201)


@rag_bp.post("/query")
@jwt_required()
def query():
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}
    document_id = payload.get("document_id")
    question = payload.get("question")
    if not document_id or not question:
        raise APIError("VALIDATION_ERROR", "document_id and question are required.", 400)
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        raise APIError("NOT_FOUND", "Document was not found.", 404)
    result = query_document(document, question)
    log_activity(user_id, "rag_query", document.title)
    db.session.commit()
    return success(result, result.get("message") or "Answer generated from retrieved context.")

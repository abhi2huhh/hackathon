from __future__ import annotations

import os
import re
import uuid
from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.utils.error_handlers import APIError

EXTENSION_MIME = {
    "pdf": {"application/pdf", "application/octet-stream"},
    "docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/octet-stream",
        "application/zip",
    },
    "txt": {"text/plain", "application/octet-stream"},
}


def ensure_upload_dir() -> Path:
    folder = Path(current_app.config["UPLOAD_FOLDER"])
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def validate_upload(file: FileStorage | None, allowed: set[str] | None = None) -> str:
    if file is None or not file.filename:
        raise APIError("VALIDATION_ERROR", "A file upload is required.", 400)
    name = secure_filename(file.filename)
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    allowed = allowed or current_app.config["ALLOWED_EXTENSIONS"]
    if ext not in allowed:
        raise APIError(
            "UNSUPPORTED_FORMAT",
            f"Unsupported file type '.{ext}'. Allowed types: {', '.join(sorted(allowed))}.",
            400,
        )
    mime = (file.mimetype or "").lower()
    if mime and mime not in current_app.config["ALLOWED_MIME_TYPES"] and mime not in EXTENSION_MIME.get(ext, set()):
        raise APIError("UNSUPPORTED_FORMAT", "The file MIME type is not permitted.", 400)
    return ext


def save_upload(file: FileStorage, allowed: set[str] | None = None) -> tuple[str, str, str]:
    ext = validate_upload(file, allowed)
    original = secure_filename(file.filename)
    stored = f"{uuid.uuid4().hex}.{ext}"
    dest = ensure_upload_dir() / stored
    file.save(dest)
    return original, stored, str(dest)


def safe_path(stored_filename: str) -> Path:
    folder = ensure_upload_dir().resolve()
    target = (folder / stored_filename).resolve()
    if folder not in target.parents and target != folder:
        raise APIError("FORBIDDEN", "Invalid file path.", 403)
    return target


def remove_file(stored_filename: str) -> None:
    try:
        path = safe_path(stored_filename)
        if path.exists():
            os.remove(path)
    except OSError:
        pass

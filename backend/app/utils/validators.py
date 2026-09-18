from __future__ import annotations

import re

from email_validator import EmailNotValidError, validate_email

from app.utils.error_handlers import APIError


def require_fields(payload: dict, fields: list[str]) -> None:
    missing = [f for f in fields if payload.get(f) in (None, "")]
    if missing:
        raise APIError(
            "VALIDATION_ERROR",
            f"Missing required field(s): {', '.join(missing)}.",
            400,
            {"fields": missing},
        )


def parse_email(value: str) -> str:
    try:
        result = validate_email(value, check_deliverability=False)
        return result.normalized
    except EmailNotValidError as exc:
        raise APIError("VALIDATION_ERROR", str(exc), 400) from exc


def parse_password(value: str) -> str:
    if not value or len(value) < 8:
        raise APIError("VALIDATION_ERROR", "Password must be at least 8 characters.", 400)
    return value


def clamp_int(value, minimum: int, maximum: int, name: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise APIError("VALIDATION_ERROR", f"{name} must be an integer.", 400) from exc
    if number < minimum or number > maximum:
        raise APIError(
            "VALIDATION_ERROR",
            f"{name} must be between {minimum} and {maximum}.",
            400,
        )
    return number


def sanitize_query(value: str, max_len: int = 400) -> str:
    text = re.sub(r"\s+", " ", (value or "")).strip()
    return text[:max_len]

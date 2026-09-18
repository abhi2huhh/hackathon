from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.extensions import db, limiter
from app.models.role import Role
from app.models.user import User
from app.utils.activity import log_activity
from app.utils.error_handlers import APIError, success
from app.utils.validators import parse_email, parse_password, require_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
@limiter.limit("10 per minute")
def register():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, ["name", "email", "password"])
    email = parse_email(payload["email"])
    if User.query.filter_by(email=email).first():
        raise APIError("CONFLICT", "An account with this email already exists.", 409)
    user = User(name=payload["name"].strip()[:120], email=email, role=Role.USER)
    user.set_password(parse_password(payload["password"]))
    db.session.add(user)
    log_activity(None, "register", email)
    db.session.commit()
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return success({"user": user.to_dict(), "access_token": token}, "Account created.", 201)


@auth_bp.post("/login")
@limiter.limit("20 per minute")
def login():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, ["email", "password"])
    email = parse_email(payload["email"])
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(payload["password"]):
        raise APIError("UNAUTHORIZED", "Invalid email or password.", 401)
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    log_activity(user.id, "login", None)
    db.session.commit()
    return success({"user": user.to_dict(), "access_token": token}, "Signed in.")


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return success({}, "Signed out. Discard the access token on the client.")


@auth_bp.get("/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        raise APIError("UNAUTHORIZED", "User no longer exists.", 401)
    return success(user.to_dict())

from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.models.role import Role
from app.utils.error_handlers import APIError


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in roles:
                raise APIError("FORBIDDEN", "Administrator access is required.", 403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required(Role.ADMIN)

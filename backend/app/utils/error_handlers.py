from flask import jsonify


def success(data=None, message: str = "", status: int = 200):
    return jsonify({"success": True, "data": data if data is not None else {}, "message": message}), status


def error(code: str, message: str, status: int = 400, details=None):
    payload = {"success": False, "error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return jsonify(payload), status


class APIError(Exception):
    def __init__(self, code: str, message: str, status: int = 400, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err: APIError):
        return error(err.code, err.message, err.status, err.details)

    @app.errorhandler(400)
    def handle_400(_err):
        return error("BAD_REQUEST", "The request could not be understood.", 400)

    @app.errorhandler(401)
    def handle_401(_err):
        return error("UNAUTHORIZED", "Authentication is required.", 401)

    @app.errorhandler(403)
    def handle_403(_err):
        return error("FORBIDDEN", "You do not have permission to perform this action.", 403)

    @app.errorhandler(404)
    def handle_404(_err):
        return error("NOT_FOUND", "The requested resource was not found.", 404)

    @app.errorhandler(413)
    def handle_413(_err):
        return error("FILE_TOO_LARGE", "Uploaded file exceeds the 10MB size limit.", 413)

    @app.errorhandler(429)
    def handle_429(_err):
        return error("RATE_LIMITED", "Too many requests. Please wait and try again.", 429)

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        app.logger.exception("Unhandled error: %s", type(err).__name__)
        if app.config.get("DEBUG"):
            return error("INTERNAL_ERROR", str(err), 500)
        return error("INTERNAL_ERROR", "An unexpected server error occurred.", 500)

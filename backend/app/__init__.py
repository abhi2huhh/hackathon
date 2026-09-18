from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt, limiter, migrate
from app.utils.error_handlers import register_error_handlers


def create_app(config_object=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    if app.config.get("TESTING") or app.config.get("RATELIMIT_ENABLED") is False:
        limiter.enabled = False
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    from app.models import (  # noqa: F401
        activity_log,
        bookmark,
        document,
        document_chunk,
        job_role,
        resource,
        resume,
        roadmap,
        roadmap_step,
        summary,
        user,
        user_progress,
    )

    from app.routes.admin import admin_bp
    from app.routes.ats import ats_bp
    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    from app.routes.rag import rag_bp
    from app.routes.resources import resources_bp
    from app.routes.roadmaps import roadmaps_bp
    from app.routes.search import search_bp
    from app.routes.summarization import summarization_bp
    from app.routes.users import users_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(ats_bp, url_prefix="/api/ats")
    app.register_blueprint(summarization_bp, url_prefix="/api/summarization")
    app.register_blueprint(rag_bp, url_prefix="/api/rag")
    app.register_blueprint(roadmaps_bp, url_prefix="/api/roadmaps")
    app.register_blueprint(resources_bp, url_prefix="/api/resources")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    register_error_handlers(app)

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    return app

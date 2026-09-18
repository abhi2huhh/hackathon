import io
import json

import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models.role import Role
from app.models.user import User
from app.seed import seed


@pytest.fixture()
def app():
    application = create_app(TestingConfig)
    application.config["RATELIMIT_ENABLED"] = False
    with application.app_context():
        db.create_all()
        seed()
        user = User(name="Ada Lovelace", email="ada@example.com", role=Role.USER)
        user.set_password("password123")
        admin = User(name="Admin", email="admin@example.com", role=Role.ADMIN)
        admin.set_password("password123")
        db.session.add_all([user, admin])
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_header(client):
    response = client.post("/api/auth/login", json={"email": "ada@example.com", "password": "password123"})
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

from __future__ import annotations

from datetime import datetime, timezone

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User

try:
    from pymongo import MongoClient
    from pymongo.errors import DuplicateKeyError
except ImportError:  # Local SQL-only development remains supported.
    MongoClient = None
    DuplicateKeyError = Exception


_client = None


def mongo_enabled() -> bool:
    return bool(current_app.config.get("MONGODB_URI"))


def _collection():
    global _client
    if not mongo_enabled() or MongoClient is None:
        return None
    if _client is None:
        _client = MongoClient(
            current_app.config["MONGODB_URI"],
            serverSelectionTimeoutMS=current_app.config["MONGODB_TIMEOUT_MS"],
        )
    collection = _client[current_app.config["MONGODB_DATABASE"]][
        current_app.config["MONGODB_AUTH_COLLECTION"]
    ]
    collection.create_index("email", unique=True)
    return collection


def create_or_sync(user: User) -> None:
    collection = _collection()
    if collection is None:
        return
    now = datetime.now(timezone.utc)
    collection.update_one(
        {"sql_user_id": user.id},
        {
            "$set": {
                "name": user.name,
                "email": user.email,
                "password_hash": user.password_hash,
                "role": user.role,
                "updated_at": now,
            },
            "$setOnInsert": {"sql_user_id": user.id, "created_at": now},
        },
        upsert=True,
    )


def create_new(user: User) -> None:
    collection = _collection()
    if collection is None:
        return
    now = datetime.now(timezone.utc)
    try:
        collection.insert_one(
            {
                "sql_user_id": user.id,
                "name": user.name,
                "email": user.email,
                "password_hash": user.password_hash,
                "role": user.role,
                "created_at": now,
                "updated_at": now,
            }
        )
    except DuplicateKeyError:
        raise ValueError("An account with this email already exists.")


def authenticate(email: str, password: str, user: User) -> bool:
    collection = _collection()
    if collection is None:
        return user.check_password(password)
    record = collection.find_one({"email": email})
    if record is None:
        create_or_sync(user)
        record = collection.find_one({"email": email})
    return bool(record and check_password_hash(record["password_hash"], password))


def sync_role(user: User) -> None:
    collection = _collection()
    if collection is not None:
        collection.update_one(
            {"sql_user_id": user.id},
            {"$set": {"role": user.role, "updated_at": datetime.now(timezone.utc)}},
        )
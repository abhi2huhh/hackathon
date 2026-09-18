from app.extensions import db


class Role:
    USER = "USER"
    ADMIN = "ADMIN"

    ALL = (USER, ADMIN)

from flask.cli import FlaskGroup
from app import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

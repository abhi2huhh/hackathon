from app import create_app
from app.extensions import db
from app.seed import seed

app = create_app()
with app.app_context():
    db.create_all()
    seed()
    print("Database tables created and seed data loaded.")

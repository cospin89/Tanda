from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    from .models.User import User

    with app.app_context():
        db.create_all()

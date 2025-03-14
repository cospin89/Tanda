# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import mail

def create_app():
    app = Flask(__name__)
    
    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-email-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'
    mail.init_app(app)
    
    load_dotenv()
    app.secret_key = os.getenv("app_secret")
    
    # Database setup
    from .database import init_db
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_connection_string')
    init_db(app)
    
    # Register blueprints
    from .login import login_bp as login_blueprint
    app.register_blueprint(login_blueprint)
    
    # Register blueprints
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app
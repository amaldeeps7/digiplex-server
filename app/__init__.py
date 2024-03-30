from flask import Flask
from config import Config
from .extensions import db  # Import db from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Initialize db with the app

    with app.app_context():
        db.create_all()  # Create database tables for our data models

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

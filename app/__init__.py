from flask import Flask
from .config import Config
from .extensions.mongo import init_mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    init_mongo(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

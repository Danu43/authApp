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
    from app.routes.page_routes import page_bp
    from app.routes.upload_routes import upload_bp
    from app.routes.pdf_routes import pdf_bp
    
    app.register_blueprint(pdf_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(upload_bp)

    return app

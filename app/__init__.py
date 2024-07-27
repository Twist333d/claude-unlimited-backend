from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.logger import logger
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    logger.info("Initializing Flask application")

    # Setup CORS
    cors_origins = os.environ.get('CORS_ORIGINS', '').split(',')
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now

    from .routes import main
    app.register_blueprint(main)
    logger.info("Registered main blueprint")

    # Ensure exceptions are propagated to the logger
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
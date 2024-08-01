from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.logger import logger
from supabase import create_client, Client
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    logger.info("Initializing Flask application")

    logger.info("Initializing Supabase client")

    try:
        url = app.config['SUPABASE_URL']
        key = app.config['SUPABASE_KEY']
        app.supabase = create_client(url, key)
        logger.info(f"Successfully connected to Supabase at {url}")
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {str(e)}")


    # Setup CORS
    cors_origins = os.environ.get('CORS_ORIGINS', '').split(',')
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now

    from .routes import main
    app.register_blueprint(main)
    logger.info("Registered main blueprint")

    # Add a test route
    @app.route('/test_db')
    def test_db():
        try:
            # Perform a simple query
            result = app.supabase.table('conversations').select('id').limit(1).execute()
            return f"Database connection successful. Result: {result.data}", 200
        except Exception as e:
            return f"Database connection failed: {str(e)}", 500

    # Ensure exceptions are propagated to the logger
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
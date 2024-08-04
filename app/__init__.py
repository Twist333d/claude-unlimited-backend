from flask import Flask
from flask_cors import CORS
from .config import Config
from .utils.logger import logger
from supabase import create_client, Client
import os

# Global Supabase client
supabase_client: Client = None

def create_app(config_class=Config):
    global supabase_client
    app = Flask(__name__)
    app.config.from_object(config_class)
    logger.info(f"Loaded configuration: {type(app.config).__name__}")
    CORS(app)

    logger.info("Initializing Flask application")


    logger.info("Initializing Supabase client")

    try:
        url = app.config['SUPABASE_URL']
        key = app.config['SUPABASE_KEY']
        supabase_client = create_client(url, key)
        logger.info(f"Successfully connected to Supabase at {url}")
        app.supabase = supabase_client

        # Test the connection without relying on existing data
        test_response = app.supabase.table('conversations').select('count').execute()
        row_count = test_response.count
        logger.info(f"Successfully connected to Supabase. Conversations table has {row_count} rows.")

    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        logger.error(f"Supabase URL: {url}")  # Don't log the full key for security reasons
        logger.error(f"Supabase Key: {key[:5]}...{key[-5:] if key else ''}")
        # You might want to raise an exception here if Supabase connection is critical for your app
        raise RuntimeError(f"Failed to initialize Supabase: {str(e)}")

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
            # Perform a simple query that doesn't rely on existing data
            result = app.supabase.table('conversations').select('count').execute()
            row_count = result.count
            return f"Database connection successful. Conversations table has {row_count} rows.", 200
        except Exception as e:
            return f"Database connection failed: {str(e)}", 500

    # Ensure exceptions are propagated to the logger
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
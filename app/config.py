import os
import logging
from dotenv import load_dotenv

# Load .env file only in development
if os.getenv('FLASK_ENV') != 'production':
    load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    MAX_TOKENS = 4096
    MAX_HISTORY_TOKENS = 150000
    PORT = int(os.getenv('PORT', 5001))

    # Supabase keys
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Auth
    SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

    # Setup CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Use DEBUG instead of FLASK_ENV
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Logging configuration
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'app.log'

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class StagingConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.INFO

config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    flask_env = os.getenv('FLASK_ENV', 'development')
    return config.get(flask_env, config['default'])
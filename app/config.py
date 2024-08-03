import os
import logging
from dotenv import load_dotenv


load_dotenv() # load the .env file



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

    # Environment configuration
    ENV = os.getenv('ENV', 'development') # default to production, unless there is an .env file
    DEBUG = ENV != 'production'

    # Different OS
    OS_TYPE = os.getenv("OS_TYPE", 'PC')

    # Logging configuration
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'app.log'

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class StagingConfig(Config):
    ENV = 'staging'
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    LOG_LEVEL = logging.INFO

config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.getenv('ENV', 'development')
    return config.get(env, config['default'])
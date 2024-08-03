import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    MAX_TOKENS = 8192 #increased to maximum supported tokens
    MAX_HISTORY_TOKENS = 10000  # 5% of Claude 3 Sonnet's context window
    PORT = int(os.getenv('PORT', 5001))

    # Get SUPABASE env
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

    # Setup CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Use DEBUG instead of FLASK_ENV
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Logging configuration
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'app.log'

    # to re-factor this -> I am switching to Supabase
    # Database URL for Heroku or local SQLite
    #DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_NAME}')
    #if DATABASE_URL.startswith("postgres://"):
    #    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


config = Config()
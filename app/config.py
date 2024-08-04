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
    PORT = int(os.getenv('PORT', 5000))  # Consistently use 5000 as default
    BASE_URL = os.getenv('BASE_URL', f'http://localhost:{PORT}')

    # Supabase keys
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Auth
    SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

    # Setup CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Environment configuration
    ENV = os.getenv('ENV', 'development') # default to development, unless there is an .env file
    DEBUG = ENV != 'production'

    # Different OS
    OS_TYPE = os.getenv("OS_TYPE", 'PC')

    # Logging configuration
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'app.log'

    # Environment-specific test data
    TEST_USER_ID = os.getenv('TEST_USER_ID')
    TEST_CONVERSATION_ID = os.getenv('TEST_CONVERSATION_ID')

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    TEST_USER_ID = os.getenv('TEST_USER_ID', 'fbba4a13-b4bb-4b99-9118-1acec1b2d240' if os.getenv(
        'OS_TYPE') != 'PC' else '9ac4d55a-beb5-476a-8724-9cc3eb3aee5a')
    TEST_CONVERSATION_ID = os.getenv('TEST_CONVERSATION_ID', 'c69abff2-a41a-46ff-8c77-e617141765a3' if os.getenv(
        'OS_TYPE') != 'PC' else 'ce4f00d4-928b-40bd-b71a-03ad623501ed')

class TestConfig(Config):
    TESTING = True
    TEST_USER_ID = os.getenv('TEST_USER_ID', 'fbba4a13-b4bb-4b99-9118-1acec1b2d240' if os.getenv(
        'OS_TYPE') != 'PC' else '9ac4d55a-beb5-476a-8724-9cc3eb3aee5a')
    TEST_CONVERSATION_ID = os.getenv('TEST_CONVERSATION_ID', 'c69abff2-a41a-46ff-8c77-e617141765a3' if os.getenv(
        'OS_TYPE') != 'PC' else 'ce4f00d4-928b-40bd-b71a-03ad623501ed')

class StagingConfig(Config):
    ENV = 'staging'
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    TEST_USER_ID = os.environ.get('STAGING_TEST_USER_ID', '60ae0ff0-f46e-448f-b57c-f3ddfb00f107')
    TEST_CONVERSATION_ID = os.environ.get('STAGING_TEST_CONVERSATION_ID', '4455c4d7-82b3-4cbd-be08-831d60dc5fb1')

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    LOG_LEVEL = logging.INFO
    TEST_USER_ID = '51a3ad18-76cb-46e2-bda8-268c634550a2'
    TEST_CONVERSATION_ID = 'e7c0daf8-90fc-44d6-bb03-30cb889dabcd'

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.getenv('ENV', 'development')
    return config.get(env, config['default'])
import os
import logging
from dotenv import load_dotenv

load_dotenv() # load the .env file


class Config:
    # APP SETUP
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_ENV = os.getenv('APP_ENV', 'development') # default to development, unless there is an .env file
    APP_DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
    APP_PORT = int(os.getenv('PORT', 5000))  # Consistently use 5000 as default
    OS_TYPE = os.getenv("OS_TYPE", 'PC')

    # ANTHROPIC SETUP
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    MAX_TOKENS = 4096
    MAX_HISTORY_TOKENS = 150000

    # API SETUP
    APP_BASE_URL = os.getenv('APP_BASE_URL', f'http://localhost:{APP_PORT}')

    # SUPABASE SETUP
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

    # CORS SETUP
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002').split(',')

    # LOGGING SETUP
    LOG_LEVEL = logging.DEBUG if APP_DEBUG else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'app.log'

    # CUSTOM USERS AND CONVERSATION SETUP
    TEST_USER_ID = os.getenv('TEST_USER_ID')
    TEST_CONVERSATION_ID = os.getenv('TEST_CONVERSATION_ID')

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    APP_ENV = 'development'
    APP_DEBUG = True
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
    APP_ENV = 'staging'
    APP_DEBUG = True
    LOG_LEVEL = logging.DEBUG
    TEST_USER_ID = os.environ.get('TEST_USER_ID')
    TEST_CONVERSATION_ID = os.environ.get('TEST_CONVERSATION_ID')

class ProductionConfig(Config):
    APP_ENV = 'production'
    APP_DEBUG = False
    LOG_LEVEL = logging.INFO
    TEST_USER_ID = os.environ.get('TEST_USER_ID')
    TEST_CONVERSATION_ID = os.environ.get('TEST_CONVERSATION_ID')

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    if config_name is None:
        config_name = os.getenv('APP_ENV', 'default')
    return config.get(config_name, config['default'])
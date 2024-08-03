from app import create_app
from app.utils.logger import logger
from app.config import get_config

current_config = get_config()
application = create_app()

if __name__ == '__main__':
    debug = current_config.DEBUG
    env = current_config.ENV
    log_level = current_config.LOG_LEVEL
    logger.info(f'Application started with the following settings: \n'
                f'- Debug: {debug}, \n'
                f'- Environment: {env}, \n'
                f'- Log level: {log_level}.')
    application.run(host='0.0.0.0', port=current_config.PORT, debug=debug)
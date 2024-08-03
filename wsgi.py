from app import create_app
from app.utils.logger import logger
from app.config import config

current_config = config.get(config.get('FLASK_ENV', 'development'))
application = create_app()

if __name__ == '__main__':
    debug = current_config.DEBUG
    logger.info('Application started')
    application.run(host='0.0.0.0', port=current_config.PORT, debug=debug)
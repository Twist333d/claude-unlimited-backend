from app import create_app
from app.utils.logger import logger
from app.config import config

application = create_app()

if __name__ == '__main__':
    debug = config.DEBUG
    logger.info('Application started')
    application.run(host='0.0.0.0', port=config.PORT, debug=debug)
import os
from backend.app import create_app
from backend.app.utils.database import init_db
from backend.app.utils.logger import logger
from backend.app.config import config

app = create_app()

if __name__ == '__main__':
    if __name__ == '__main__':
        with app.app_context():
            init_db()

        debug = config.DEBUG
        logger.info('Application started')
        app.run(host='0.0.0.0', port=config.PORT, debug=debug)
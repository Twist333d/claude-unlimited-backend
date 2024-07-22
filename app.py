from app import create_app
from app.utils.database import init_db
from app.utils.logger import logger
from app.config import config
from flask_cors import CORS

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()

    # setup CORS
    CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})

    debug = config.DEBUG
    logger.info('Application started')
    app.run(host='0.0.0.0', port=config.PORT, debug=debug)
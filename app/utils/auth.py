from flask import request, current_app
from functools import wraps
import jwt as pyjwt

def get_test_user_id():
    if current_app.config['APP_ENV'] in ['development', 'staging']:
        return current_app.config['TEST_USER_ID']
    return None

def get_user_id_from_request():
    # For development and staging, use test user ID if we're running tests
    if current_app.config['APP_ENV'] in ['development', 'staging'] and current_app.config.get('TESTING', False):
        return get_test_user_id()

    # For all other cases (including production), use the auth header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    try:
        # Extract the token from the Authorization header
        token = auth_header.split(' ')[1]

        # Decode and verify the JWT token
        decoded_token = pyjwt.decode(token, current_app.config['SUPABASE_JWT_SECRET'], algorithms=["HS256"])
        return decoded_token['sub']  # 'sub' is the user ID in Supabase JWTs
    except pyjwt.InvalidTokenError:
        current_app.logger.error("Invalid token")
        return None
    except Exception as e:
        current_app.logger.error(f"Error authenticating user: {str(e)}")
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_id_from_request()
        if user_id is None:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return decorated_function

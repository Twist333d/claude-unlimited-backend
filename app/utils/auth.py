from flask import request, current_app
from functools import wraps
import jwt


def get_user_id_from_request():
    if current_app.config['FLASK_ENV'] == 'development':
        return "fbba4a13-b4bb-4b99-9118-1acec1b2d240"  # Your test user ID

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    try:
        # Extract the token from the Authorization header
        token = auth_header.split(' ')[1]

        # Decode and verify the JWT token
        decoded_token = jwt.decode(token, current_app.config['SUPABASE_JWT_SECRET'], algorithms=["HS256"])
        return decoded_token['sub']  # 'sub' is the user ID in Supabase JWTs
    except jwt.InvalidTokenError:
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


# For local development
def get_test_user_id():
    if current_app.config['FLASK_ENV'] == 'development':
        return "fbba4a13-b4bb-4b99-9118-1acec1b2d240"  # Replace with a real Supabase user ID for testing
    return None
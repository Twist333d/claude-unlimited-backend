from flask import request, current_app
from functools import wraps
from .logger import logger


def get_user_id_from_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    try:
        token = auth_header.split(' ')[1]
        user = current_app.supabase.auth.get_user(token)
        user_id = user.user.id
        logger.info(f"Authenticated user ID: {user_id}")
        return user_id
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_id_from_request()
        if user_id is None:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return decorated_function


def get_or_create_user(supabase_client, email, password):
    # Try to sign in
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user, response.session.access_token
    except:
        # If sign in fails, try to sign up
        response = supabase_client.auth.sign_up({
            "email": email,
            "password": password
        })
        return response.user, response.session.access_token
from flask import current_app
from .logger import logger
from functools import wraps
import uuid
from datetime import datetime, timezone, date
from app import supabase_client


# Create decorator function to call each data operation
def supabase_operation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Supabase operation error in {f.__name__}: {str(e)}")
            raise
    return decorated_function

# CONVERSATION OPERATIONS
@supabase_operation
def create_conversation(user_id: str, title: str):
    logger.info(f"Creating new conversation for user {user_id}")
    conversation_id = str(uuid.uuid4())

    try:
        response = supabase_client.table('conversations').insert({
            "id": conversation_id,
            "user_id": user_id,
            "title": title,
        }).execute()

        if response.data:
            created_conversation = response.data[0]
            logger.info(f"Conversation created successfully: {created_conversation['id']}")
            return created_conversation['id']
        else:
            logger.error("No data returned from Supabase after conversation creation")
            return None

    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        return None

@supabase_operation
def get_user_conversations(user_id=None):

    query = supabase_client.table('conversations').select(
        'id',
        'created_at',
        'updated_at',
        'title',
        'last_message_at',
        'is_archived'
    ).eq('user_id', user_id).order('last_message_at', desc=True)

    if user_id:
        query = query.eq('user_id', user_id)

    response = query.execute()
    response = response.data
    logger.debug(f"Supabase response: {response}")

    return response


@supabase_operation
def get_messages_for_conversation(conversation_id, limit=50):
    logger.info(f"Fetching messages for conversation ID: {conversation_id}")
    #supabase = current_app.supabase

    query = supabase_client.table('messages').select(
        'id',
        'role',
        'content',
        'created_at'
    ).eq('conversation_id', conversation_id).order('created_at', desc=True).limit(limit)

    response = query.execute()

    response = query.execute()
    data = response.data if hasattr(response, 'data') else response

    return list(reversed(data))  # Reverse to get chronological order



@supabase_operation
def archive_conversation(conversation_id: str, archive: bool = True):
    logger.info(f"{'Archiving' if archive else 'Unarchiving'} conversation with id: {conversation_id}")

    response = supabase_client.table('conversations') \
        .update({"is_archived": archive}) \
        .eq("id", conversation_id) \
        .execute()

    data = response.data if hasattr(response, 'data') else response

    logger.info(f"Conversation {'archived' if archive else 'unarchived'} successfully: {conversation_id}")
    return data[0] if data else None
# example usage archivd_converation = archive_conversation("conversation_id"

from datetime import datetime, timezone

# Call this function when a new message arrives as we will neede it for Frontend.
@supabase_operation
def update_conversation_last_message(conversation_id: str):
    logger.info(f"Updating last_message_at for conversation: {conversation_id}")

    current_time = datetime.now(timezone.utc)

    response = supabase_client.table('conversations') \
        .update({"last_message_at": current_time.isoformat()}) \
        .eq("id", conversation_id) \
        .execute()

    data = response.data if hasattr(response, 'data') else response

    logger.info(f"last_message_at updated successfully for conversation: {conversation_id}")
    return data[0] if data else None


VALID_ROLES =['user', 'assistant', 'system']

@supabase_operation
def create_message(conversation_id: str, role: str, content: str, tokens: int = None):

    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role. Must be one of {VALID_ROLES}")

    logger.info(f"Creating new message for conversation: {conversation_id}")

    message_data = {
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tokens": tokens,
    }

    response = supabase_client.table('messages').insert(message_data).execute()
    data = response.data if hasattr(response, 'data') else response

    logger.info(f"Message created successfully with id: {data[0]['id']}")
    return data[0]


@supabase_operation
def get_message(message_id: str):
    logger.info(f"Fetching message with id: {message_id}")

    response = supabase_client.table('messages').select('*').eq('id', message_id).execute()
    data = response.data if hasattr(response, 'data') else response
    return data[0] if data else None


# USAGE STATS OPERATIONS
def increment_usage_stats(user_id, conversation_id, input_tokens, output_tokens, total_cost):
    current_date = date.today().isoformat()
    current_time = datetime.now(timezone.utc).isoformat()

    response = supabase_client.table('usage_stats').select('id, input_tokens, output_tokens, total_cost') \
        .eq('user_id', user_id) \
        .eq('conversation_id', conversation_id) \
        .eq('date', current_date) \
        .execute()

    data = response.data

    if data:
        existing_record = data[0]
        updated_data = {
            "input_tokens": existing_record['input_tokens'] + input_tokens,
            "output_tokens": existing_record['output_tokens'] + output_tokens,
            "total_cost": existing_record['total_cost'] + total_cost,
            "updated_at": current_time
        }
        response = supabase_client.table('usage_stats').update(updated_data) \
            .eq('id', existing_record['id']) \
            .execute()
    else:
        response = supabase_client.table('usage_stats').insert({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "date": current_date,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost,
            "created_at": current_time,
            "updated_at": current_time
        }).execute()

    return response.data[0] if response.data else None


def get_usage_stats(user_id=None, conversation_id=None):
    query = supabase_client.table('usage_stats').select('date, input_tokens, output_tokens, total_cost')

    if conversation_id:
        query = query.eq('conversation_id', conversation_id)
    if user_id:
        query = query.eq('user_id', user_id)

    response = query.execute()
    data = response.data

    if not data:
        return {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0,
        }

    result = {
        "total_input_tokens": sum(item['input_tokens'] for item in data),
        "total_output_tokens": sum(item['output_tokens'] for item in data),
        "total_tokens": sum(item['input_tokens'] + item['output_tokens'] for item in data),
        "total_cost": sum(item['total_cost'] for item in data),
    }

    return result

# USAGE SETTINGS OPERATIONS
@supabase_operation
def get_or_create_user_settings(user_id: str):
    response = supabase_client.table('user_settings').select('*').eq('user_id', user_id).execute()

    data = response.data if hasattr(response, 'data') else response

    if not data:
        # Create new user settings if not exist
        response = supabase_client.table('user_settings').insert({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).execute()

    data = response.data if hasattr(response, 'data') else response

    return data[0]


@supabase_operation
def update_user_settings(user_id: str, custom_instructions: str = None, preferred_model: str = None):
    update_data = {
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    if custom_instructions is not None:
        update_data["custom_instructions"] = custom_instructions
    if preferred_model is not None:
        update_data["preferred_model"] = preferred_model

    response = supabase_client.table('user_settings').update(update_data).eq('user_id', user_id).execute()

    data = response.data if hasattr(response, 'data') else response

    return data[0]
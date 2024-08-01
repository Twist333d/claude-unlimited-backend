from flask import current_app
from .logger import logger
from functools import wraps
import uuid
from datetime import datetime, timezone, date
from app import supabase_client

# TODO -> convert all to use response = instead of data, error

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

# Conversation create, update, delete, archive
@supabase_operation
def create_conversation(user_id: str, title: str = "New Conversation"):
    logger.info(f"Creating new conversation for user {user_id}")
    conversation_id = str(uuid.uuid4())

    response = supabase_client.table('conversations').insert({
        "id": conversation_id,
        "user_id": user_id,
        "title" : title,
    }).execute()

    return response[0]['id'] if response else None

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

    data, error = query.execute()

    if error:
        logger.error(f"Error fetching messages: {error}")
        raise Exception(f"Error fetching messages: {error}")

    return list(reversed(data))  # Reverse to get chronological order



@supabase_operation
def archive_conversation(conversation_id: str, archive: bool = True):
    logger.info(f"{'Archiving' if archive else 'Unarchiving'} conversation with id: {conversation_id}")

    data, error = supabase_client.table('conversations') \
        .update({"is_archived": archive}) \
        .eq("id", conversation_id) \
        .execute()

    if error:
        logger.error(f"Error {'archiving' if archive else 'unarchiving'} conversation: {error}")
        raise Exception(f"Error {'archiving' if archive else 'unarchiving'} conversation: {error}")

    logger.info(f"Conversation {'archived' if archive else 'unarchived'} successfully: {conversation_id}")
    return data[0] if data else None
# example usage archivd_converation = archive_conversation("conversation_id"

from datetime import datetime, timezone

# Call this function when a new message arrives as we will neede it for Frontend.
@supabase_operation
def update_conversation_last_message(conversation_id: str):
    logger.info(f"Updating last_message_at for conversation: {conversation_id}")

    current_time = datetime.now(timezone.utc)

    data, error = supabase_client.table('conversations') \
        .update({"last_message_at": current_time.isoformat()}) \
        .eq("id", conversation_id) \
        .execute()

    if error:
        logger.error(f"Error updating last_message_at: {error}")
        raise Exception(f"Error updating last_message_at: {error}")

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

    data, error = supabase_client.table('messages').insert(message_data).execute()

    if error:
        logger.error(f"Error creating message: {error}")
        raise Exception(f"Error creating message: {error}")

    logger.info(f"Message created successfully with id: {data[0]['id']}")
    return data[0]


@supabase_operation
def get_message(message_id: str):
    logger.info(f"Fetching message with id: {message_id}")

    data, error = supabase_client.table('messages').select('*').eq('id', message_id).execute()

    if error:
        logger.error(f"Error fetching message: {error}")
        raise Exception(f"Error fetching message: {error}")

    return data[0] if data else None



@supabase_operation
def save_usage_stats(user_id: str, conversation_id: str, total_tokens: int, total_cost: float):
    logger.info(f"Saving usage stats for user {user_id}, conversation {conversation_id}")

    current_date = date.today().isoformat()
    current_time = datetime.now(timezone.utc).isoformat()

    # Check if there's an existing record for this user, conversation, and date
    data, error = supabase_client.table('usage_stats').select('id, total_tokens, total_cost') \
        .eq('user_id', user_id) \
        .eq('conversation_id', conversation_id) \
        .eq('date', current_date) \
        .execute()

    if error:
        logger.error(f"Error checking existing usage stats: {error}")
        raise Exception(f"Error checking existing usage stats: {error}")

    if data:
        # Update existing record
        existing_record = data[0]
        updated_data = {
            "total_tokens": existing_record['total_tokens'] + total_tokens,
            "total_cost": existing_record['total_cost'] + total_cost
        }
        data, error = supabase_client.table('usage_stats').update(updated_data) \
            .eq('id', existing_record['id']) \
            .execute()
    else:
        # Insert new record
        data, error = supabase_client.table('usage_stats').insert({
            "user_id": user_id,
            "conversation_id": conversation_id,
            "date": current_date,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
        }).execute()

    if error:
        logger.error(f"Error saving usage stats: {error}")
        raise Exception(f"Error saving usage stats: {error}")

    logger.info(f"Usage stats saved successfully for user {user_id}, conversation {conversation_id}")


@supabase_operation
def get_usage_stats(user_id: str = None, conversation_id: str = None, start_date: str = None, end_date: str = None):
    logger.info(f"Fetching usage stats for user {user_id}, conversation {conversation_id}")

    query = supabase_client.table('usage_stats').select('date, total_tokens, total_cost')

    if user_id:
        query = query.eq('user_id', user_id)
    if conversation_id:
        query = query.eq('conversation_id', conversation_id)
    if start_date:
        query = query.gte('date', start_date)
    if end_date:
        query = query.lte('date', end_date)

    data, error = query.execute()

    if error:
        logger.error(f"Error fetching usage stats: {error}")
        raise Exception(f"Error fetching usage stats: {error}")

    if not data:
        logger.warning("No usage stats found")
        return None

    # Aggregate results
    result = {
        "total_tokens": sum(item['total_tokens'] for item in data),
        "total_cost": sum(item['total_cost'] for item in data),
        "daily_stats": [{
            "date": item['date'],
            "total_tokens": item['total_tokens'],
            "total_cost": item['total_cost']
        } for item in data]
    }

    logger.info("Usage stats retrieved successfully")
    return result


def update_usage_stats_after_message(user_id: str, conversation_id: str, tokens: int, cost: float):
    """
    Call this function after processing each message (both input and output).
    """
    save_usage_stats(user_id, conversation_id, tokens, cost)




@supabase_operation
def get_usage_stats(conversation_id=None):
    if conversation_id:
        logger.info(f"Fetching usage stats for conversation ID: {conversation_id}")
    else:
        logger.info("Fetching overall usage stats")

    query = supabase_client.table('usage_stats').select('''
        sum(input_tokens) as total_input,
        sum(output_tokens) as total_output,
        sum(total_tokens) as total_tokens,
        sum(input_cost) as total_input_cost,
        sum(output_cost) as total_output_cost,
        sum(total_cost) as total_cost
    ''')

    if conversation_id:
        query = query.eq('conversation_id', conversation_id)

    data, error = query.execute()

    if error:
        logger.error(f"Error fetching usage stats: {error}")
        raise Exception(f"Error fetching usage stats: {error}")

    result = data[0] if data else None

    if result:
        logger.info("Usage stats retrieved successfully")
    else:
        logger.warning("No usage stats found")

    return dict(result) if result else None


@supabase_operation
def get_or_create_user_settings(user_id: str):
    data, error = supabase_client.table('user_settings').select('*').eq('user_id', user_id).execute()

    if error:
        logger.error(f"Error fetching user settings: {error}")
        raise Exception(f"Error fetching user settings: {error}")

    if not data:
        # Create new user settings if not exist
        data, error = supabase_client.table('user_settings').insert({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).execute()

        if error:
            logger.error(f"Error creating user settings: {error}")
            raise Exception(f"Error creating user settings: {error}")

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

    data, error = supabase_client.table('user_settings').update(update_data).eq('user_id', user_id).execute()

    if error:
        logger.error(f"Error updating user settings: {error}")
        raise Exception(f"Error updating user settings: {error}")

    return data[0]
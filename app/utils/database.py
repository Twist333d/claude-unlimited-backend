from flask import current_app
from .logger import logger
from functools import wraps
import uuid

supabase = current_app.supabase


# create decorator to use for each database operation
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
def create_conversation(user_id: str, title: str = "New Conversation"):
    logger.info(f"Creating new conversation for user {user_id}")
    data = supabase.table('conversations').insert({
        "id" : str(uuid.uuid4()),
        "user_id" : user_id,
        "title" : title,
        "created_at" :
    })

# Messages create
# API keys create, update, delete
# custom instructions create, update
#
def create_conversation():
    logger.info("Creating new conversation")
    conn = create_supabase_client()
    cur = conn.cursor()
    cur.execute('INSERT INTO conversations DEFAULT VALUES')
    conversation_id = cur.lastrowid
    conn.commit()
    conn.close()
    logger.info(f"New conversation created with ID: {conversation_id}")
    return conversation_id

def save_message(conversation_id, role, content):
    logger.info(f"Saving message for conversation ID: {conversation_id}")
    role = 'user' if role in ['user', 'human'] else 'assistant'
    conn = create_supabase_client()
    conn.execute('INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                 (conversation_id, role, content))
    conn.commit()
    conn.close()
    logger.info(f"Message saved successfully for conversation ID: {conversation_id}")

def save_usage_stats(conversation_id, input_tokens, output_tokens, input_cost, output_cost):
    logger.info(f"Saving usage stats for conversation ID: {conversation_id}")
    total_tokens = input_tokens + output_tokens
    total_cost = input_cost + output_cost
    conn = create_supabase_client()
    conn.execute('''INSERT INTO usage_stats 
                    (conversation_id, input_tokens, output_tokens, total_tokens, 
                     input_cost, output_cost, total_cost) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (conversation_id, input_tokens, output_tokens, total_tokens,
                  input_cost, output_cost, total_cost))
    conn.commit()
    conn.close()
    logger.info(f"Usage stats saved successfully for conversation ID: {conversation_id}")

def get_conversations():
    logger.info("Fetching all conversations")
    conn = create_supabase_client()
    cur = conn.cursor()
    cur.execute('''SELECT c.id, c.created_at, m.content AS first_message
                   FROM conversations c
                   LEFT JOIN messages m ON c.id = m.conversation_id
                   AND m.id = (SELECT MIN(id) FROM messages WHERE conversation_id = c.id)
                   ORDER BY c.created_at DESC''')
    conversations = cur.fetchall()
    conn.close()
    logger.info(f"Retrieved {len(conversations)} conversations")
    return [dict(conv) for conv in conversations]

def get_conversations_with_details():
    conn = create_supabase_client()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.id, 
            c.created_at,
            first_message.content AS first_message,
            last_message.content AS last_message,
            last_message.timestamp AS last_message_time
        FROM conversations c
        LEFT JOIN messages first_message ON c.id = first_message.conversation_id
        AND first_message.id = (
            SELECT MIN(id)
            FROM messages
            WHERE conversation_id = c.id
        )
        LEFT JOIN messages last_message ON c.id = last_message.conversation_id
        AND last_message.id = (
            SELECT MAX(id)
            FROM messages
            WHERE conversation_id = c.id
        )
        ORDER BY last_message.timestamp DESC
    """)
    conversations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return conversations

def get_conversation_messages(conversation_id, limit=50):
    logger.info(f"Fetching messages for conversation ID: {conversation_id}")
    conn = create_supabase_client()
    cur = conn.cursor()
    cur.execute('SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?', (conversation_id, limit))
    messages = cur.fetchall()
    conn.close()
    logger.info(f"Retrieved {len(messages)} messages for conversation ID: {conversation_id}")
    return [dict(msg) for msg in reversed(messages)]

def get_usage_stats(conversation_id=None):
    if conversation_id:
        logger.info(f"Fetching usage stats for conversation ID: {conversation_id}")
    else:
        logger.info("Fetching overall usage stats")
    conn = create_supabase_client()
    cur = conn.cursor()
    if conversation_id:
        cur.execute('''SELECT SUM(input_tokens) as total_input, 
                              SUM(output_tokens) as total_output,
                              SUM(total_tokens) as total_tokens,
                              SUM(input_cost) as total_input_cost,
                              SUM(output_cost) as total_output_cost,
                              SUM(total_cost) as total_cost
                       FROM usage_stats
                       WHERE conversation_id = ?''', (conversation_id,))
    else:
        cur.execute('''SELECT SUM(input_tokens) as total_input, 
                              SUM(output_tokens) as total_output,
                              SUM(total_tokens) as total_tokens,
                              SUM(input_cost) as total_input_cost,
                              SUM(output_cost) as total_output_cost,
                              SUM(total_cost) as total_cost
                       FROM usage_stats''')
    result = cur.fetchone()
    conn.close()
    if result:
        logger.info("Usage stats retrieved successfully")
    else:
        logger.warning("No usage stats found")
    return dict(result) if result else None
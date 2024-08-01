from flask import Blueprint, request, jsonify, current_app
from .services.chat_service import process_chat_request
from .utils.database import (
    get_usage_stats, create_conversation, create_message,
    get_messages_for_conversation, get_user_conversations,
    update_conversation_last_message, archive_conversation,
    get_or_create_user_settings, update_user_settings
)
from .utils.logger import logger


main = Blueprint('main', __name__)

@main.route('/conversations', methods=['GET'])
def list_user_conversations():
    logger.info("Fetching list of conversations.")
    user_id = get_user_id_from_request()  # Implement this function to get user_id from the request
    conversations = get_user_conversations(user_id)
    return jsonify(conversations)

@main.route('/conversations', methods=['POST'])
def create_new_user_conversation():
    logger.info("Creating a new conversation")
    user_id = get_user_id_from_request()
    title = request.json.get('title', "New Conversation")
    conversation_id = create_conversation(user_id, title)
    return jsonify({"conversation_id": conversation_id})

@main.route('/conversations/<uuid:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    logger.info(f"Fetching messages for conversation {conversation_id}")
    limit = request.args.get('limit', 50, type=int)
    messages = get_messages_for_conversation(str(conversation_id), limit)
    return jsonify(messages)

@main.route('/conversations/<uuid:conversation_id>/archive', methods=['POST'])
def archive_conv(conversation_id):
    logger.info(f"Archiving conversation {conversation_id}")
    archive = request.json.get('archive', True)
    result = archive_conversation(str(conversation_id), archive)
    return jsonify(result)


@main.route('/chat', methods=['POST'])
def chat():
    logger.info(f"Received chat request: {request.json}")
    data = request.json
    user_id = get_user_id_from_request()
    conversation_id = data.get('conversation_id')
    messages = data.get('messages', [])

    if not conversation_id:
        logger.info("No conversation ID provided, creating a new conversation")
        conversation_id = create_conversation(user_id)
    else:
        conversation_id = str(conversation_id)  # Ensure it's a string

    if not messages:
        logger.warning("No messages provided in chat request")
        return jsonify({"error": "No messages provided"}), 400

    try:
        # Save new user message
        for message in messages:
            create_message(conversation_id, 'user', message)

        # Process the chat request
        result = process_chat_request(user_id, conversation_id, messages)

        # Save the assistant's response
        create_message(conversation_id, 'assistant', result['response'])

        # Update conversation's last_message_at
        update_conversation_last_message(conversation_id)

        logger.info("Chat request processed successfully")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in chat request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/usage', methods=['GET'])
def usage():
    logger.info("Received usage stats request")
    user_id = get_user_id_from_request()
    conversation_id = request.args.get('conversation_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        stats = get_usage_stats(user_id, conversation_id, start_date, end_date)
        logger.info("Usage stats retrieved successfully")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error retrieving usage stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/user/settings', methods=['GET', 'PUT'])
def user_settings():
    user_id = get_user_id_from_request()
    if request.method == 'GET':
        settings = get_or_create_user_settings(user_id)
        return jsonify(settings)
    elif request.method == 'PUT':
        data = request.json
        custom_instructions = data.get('custom_instructions')
        preferred_model = data.get('preferred_model')
        updated_settings = update_user_settings(user_id, custom_instructions, preferred_model)
        return jsonify(updated_settings)

def get_user_id_from_request():
    # Implement this function to extract the user_id from the request
    # This could involve checking an authentication token or session
    # For now, we'll just return a placeholder
    uuid = "634998e3-7687-4266-a004-8cb2f35c42ac"
    return uuid
from datetime import datetime, timezone,  timedelta

import jwt as pyjwt
from jwt.exceptions import InvalidTokenError, InvalidKeyError
from flask import Blueprint, request, jsonify, current_app
from .services.chat_service import process_chat_request
from .utils.database import (create_conversation, create_message,
    get_messages_for_conversation, get_user_conversations,
    update_conversation_last_message, archive_conversation,
    get_or_create_user_settings, update_user_settings, get_usage_stats
)
from .utils.auth import login_required, get_user_id_from_request
from .utils.logger import logger


main = Blueprint('main', __name__)

@main.route('/conversations', methods=['GET'])
@login_required
def list_user_conversations():
    logger.info("Entering list_user_conversations route")
    logger.info("Fetching list of conversations.")
    user_id = get_user_id_from_request()
    conversations = get_user_conversations(user_id)
    return jsonify(conversations)



@main.route('/conversations/<uuid:conversation_id>/messages', methods=['GET'])
@login_required
def get_conversation_messages(conversation_id):
    logger.info(f"Fetching messages for conversation {conversation_id}")
    user_id = get_user_id_from_request()
    limit = request.args.get('limit', 50, type=int)
    messages = get_messages_for_conversation(str(conversation_id), limit)
    return jsonify(messages)

@main.route('/conversations/<uuid:conversation_id>/archive', methods=['POST'])
@login_required
def archive_conv(conversation_id):
    logger.info(f"Archiving conversation {conversation_id}")
    user_id = get_user_id_from_request()
    archive = request.json.get('archive', True)
    result = archive_conversation(str(conversation_id), archive)
    return jsonify(result)


@main.route('/chat', methods=['POST'])
@login_required
def chat():
    logger.info("Entering chat route")
    logger.info(f"Received chat request: {request.json}")
    user_id = get_user_id_from_request()
    data = request.json
    conversation_id = data.get('conversation_id')
    message = data.get('message', '')

    if not message:
        logger.warning("No message received for chat request")
        return jsonify({"error": "No message provided"}), 400


    if not conversation_id:
        # Use the first 30 characters of the message as the title
        title = message[:30] + "..." if len(message) > 30 else message
        # Create a new conversation
        conversation_id = create_conversation(user_id, title)
        logger.info(f"Created new conversation {conversation_id}")


    try:
        # Save new user message
        # Now we have a conversation_id, create the message
        message_id = create_message(conversation_id, user_id, 'user', message)
        logger.info(f"Created message for user: {user_id}, conversation: {conversation_id}")

        # Process the chat request
        result = process_chat_request(user_id, conversation_id, message)

        # Save the assistant's response
        assistant_message_id = create_message(conversation_id, user_id, 'assistant', result['response'])

        # Update conversation's last_message_at
        update_conversation_last_message(conversation_id)

        # Add the conversation_id to the result
        result['conversation_id'] = conversation_id

        logger.info("Chat request processed successfully")
        return jsonify({
            "conversation_id": conversation_id,
            "message_id": message_id,
            "assistant_message_id": assistant_message_id,
            "response": result['response']
        })
    except Exception as e:
        logger.error(f"Error in chat request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/usage', methods=['GET'])
@login_required
def usage():
    logger.info("Received usage stats request")
    user_id = get_user_id_from_request()
    conversation_id = request.args.get('conversation_id')
    try:
        stats = get_usage_stats(user_id, conversation_id)
        logger.info("Usage stats retrieved successfully")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error retrieving usage stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/user/settings', methods=['GET', 'PUT'])
@login_required
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
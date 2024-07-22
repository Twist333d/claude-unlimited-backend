from flask import Blueprint, request, jsonify
from .services.chat_service import process_chat_request
from .utils.database import get_usage_stats, create_conversation, save_message, get_conversations, get_conversation_messages
from .utils.logger import logger
from backend.app.utils.database import get_conversations_with_details


main = Blueprint('main', __name__)

@main.route('/conversations', methods=['GET'])
def list_conversations():
    logger.info("Fetching list of first and last messages")
    conversations = get_conversations_with_details()
    return jsonify(conversations)

@main.route('/conversations', methods=['POST'])
def start_conversation():
    logger.info("Starting new conversation")
    conversation_id = create_conversation()
    return jsonify({"conversation_id": conversation_id})

@main.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    logger.info(f"Fetching messages for conversation {conversation_id}")
    messages = get_conversation_messages(conversation_id)
    return jsonify(messages)


@main.route('/chat', methods=['POST'])
def chat():
    logger.info(f"Received chat request: {request.json}")
    data = request.json

    conversation_id = data.get('conversation_id')
    messages = data.get('messages', [])

    logger.info(f"Conversation ID: {conversation_id}, Messages: {messages}")

    if not conversation_id:
        logger.info("No conversation ID provided, creating a new conversation")
        conversation_id = create_conversation()

    if not messages:
        logger.warning("No messages provided in chat request")
        return jsonify({"error": "No messages provided"}), 400

    try:
        # Save new user message
        for message in messages:
            save_message(conversation_id, 'user', message)

        # Process the chat request with the full conversation history
        result = process_chat_request(conversation_id, messages)

        # Save the assistant's response
        save_message(conversation_id, 'assistant', result['response'])

        logger.info("Chat request processed successfully")
        return jsonify({
            "response": result['response'],
            "input_tokens": result['input_tokens'],
            "output_tokens": result['output_tokens'],
            "total_tokens": result['total_tokens'],
            "input_cost": result['input_cost'],
            "output_cost": result['output_cost'],
            "total_cost": result['total_cost']
        })
    except Exception as e:
        logger.error(f"Error in chat request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/usage', methods=['GET'])
def usage():
    logger.info("Received usage stats request")
    conversation_id = request.args.get('conversation_id')
    try:
        stats = get_usage_stats(conversation_id)
        logger.info("Usage stats retrieved successfully")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error retrieving usage stats: {str(e)}")
        return jsonify({"error": str(e)}), 500
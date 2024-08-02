from flask import current_app
from ..services.anthropic_service import send_anthropic_request
from ..utils.database import increment_usage_stats, get_messages_for_conversation
from ..utils.logger import logger

INPUT_COST_PER_1K = 0.0015
OUTPUT_COST_PER_1K = 0.0060


def process_chat_request(user_id, conversation_id, message):
    logger.info(f"Processing chat request for conversation {conversation_id}")

    conversation_messages = get_messages_for_conversation(conversation_id)
    all_messages = prepare_messages(conversation_messages, message)

    response = send_anthropic_request(all_messages)
    logger.info(f"Response structure: {response}")  # Add this line

    assistant_message = response['content']
    input_tokens = response['input_tokens']
    output_tokens = response['output_tokens']

    input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
    output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K
    total_cost = input_cost + output_cost

    increment_usage_stats(user_id, conversation_id, input_tokens, output_tokens, total_cost)

    logger.info(f"Chat request processed for conversation {conversation_id}. "
                 f"Input tokens: {input_tokens}, Output tokens: {output_tokens}, "
                 f"Total cost: ${total_cost:.6f}")

    return {
        "response": assistant_message,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "total_cost": round(total_cost, 6)
    }


def prepare_messages(conversation_messages, new_message):
    messages = []
    for msg in conversation_messages:
        if msg['role'] in ['user', 'assistant']:
            messages.append({"role": msg['role'], "content": msg['content']})

    # Add new user message
    messages.append({"role": "user", "content": new_message})

    # Ensure messages alternate between user and assistant
    filtered_messages = []
    last_role = None
    for msg in messages:
        if msg['role'] != last_role:
            filtered_messages.append(msg)
            last_role = msg['role']

    return filtered_messages
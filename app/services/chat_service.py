from flask import current_app
from ..services.anthropic_service import send_anthropic_request
from ..utils.database import save_message, save_usage_stats, get_conversation_messages
from ..utils.logger import logger

INPUT_COST_PER_1K = 0.0015
OUTPUT_COST_PER_1K = 0.0060


def process_chat_request(conversation_id, user_message):
    logger.info(f"Processing chat request for conversation {conversation_id}")

    conversation_messages = get_conversation_messages(conversation_id)
    messages = prepare_messages(conversation_messages, [user_message])

    response = send_anthropic_request(messages)

    assistant_message = response['content']
    input_tokens = response['input_tokens']
    output_tokens = response['output_tokens']

    input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
    output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K

    save_usage_stats(conversation_id, input_tokens, output_tokens, input_cost, output_cost)

    logger.info(f"Chat request processed for conversation {conversation_id}. "
                     f"Input tokens: {input_tokens}, Output tokens: {output_tokens}, "
                     f"Total cost: ${input_cost + output_cost:.6f}")

    return {
        "response": assistant_message,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6)
    }

def prepare_messages(conversation_messages, user_messages):
    messages = []
    for msg in conversation_messages:
        if msg['role'] == 'user':
            messages.append({"role": "user", "content": msg['content']})
        elif msg['role'] == 'assistant':
            messages.append({"role": "assistant", "content": msg['content']})

    # Add new user messages
    for msg in user_messages:
        messages.append({"role": "user", "content": msg})

    # Ensure messages alternate between user and assistant
    filtered_messages = []
    last_role = None
    for msg in messages:
        if msg['role'] != last_role:
            filtered_messages.append(msg)
            last_role = msg['role']

    return filtered_messages
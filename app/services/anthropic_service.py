from anthropic import Anthropic, APIError
from flask import current_app
from ..utils.logger import logger

def send_anthropic_request(messages):
    api_key = current_app.config['ANTHROPIC_API_KEY']
    if not api_key:
        raise ValueError("Anthropic API key is not set in the configuration")

    client = Anthropic(api_key=api_key)  # Explicitly passing api_key

    logger.info(f"Sending request to Anthropic API with {len(messages)} messages")

    try:
        response = client.messages.create(
            model=current_app.config['CLAUDE_MODEL'],
            max_tokens=current_app.config['MAX_TOKENS'],
            system="You are a helpful AI assistant.",
            messages=messages
        )

        logger.info(f"Anthropic API response received. Message ID: {response.id}")

        content = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens

        logger.info(
            f"Received response from Anthropic API. Input tokens: {input_tokens}, Output tokens: {output_tokens}", extra={'component':'CHAT'})

        return {
            'content': content,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens
        }
    except APIError as e:  # Added specific exception for Anthropic API errors
        logger.error(f"Anthropic API Error: {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error in send_anthropic_request: {str(e)}", exc_info=True)
        raise
import tiktoken
from .logger import logger

def count_tokens(text):
    logger.info("Entering count_tokens function")
    try:
        logger.info("Attempting to get encoding")
        encoding = tiktoken.get_encoding("cl100k_base")
        logger.info("Encoding obtained successfully")
        token_count = len(encoding.encode(text))
        logger.info(f"Token count: {token_count}")
        return token_count
    except Exception as e:
        logger.error(f"Error in count_tokens: {str(e)}", exc_info=True)
        return len(text.split())  # Fallback to a simple word count
from anthropic import Anthropic, APIError
from flask import current_app
from ..utils.logger import logger

def send_anthropic_request(messages):
    api_key = current_app.config['ANTHROPIC_API_KEY']
    if not api_key:
        raise ValueError("Anthropic API key is not set in the configuration")

    client = Anthropic(api_key=api_key)  # Explicitly passing api_key

    logger.info(f"Sending request to Anthropic API with {len(messages)} messages")

    system_prompt = """
    You are Claude Sonnet 3.5, an advanced AI coding assistant designed to provide accurate, thoughtful, and helpful coding assistance. Your primary goal is to assist users with their programming queries and tasks while adhering to the following guidelines:

1. Provide the best, accurate, and thoughtful coding assistance possible.
2. Be extremely careful not to break existing implementations. Always consider the context and potential impact of your suggestions.
3. If you are unsure about any aspect of the user's query or the existing code, ask for clarifications before providing a solution.
4. When providing code snippets, use markdown syntax for proper formatting. Ensure that your output doesn't break the markdown + syntax support of the web frontend.
5. Structure your output in a clear and formatted way for easy readability and understanding.

When processing a user query, follow these steps:

1. Carefully read and analyze the user's query.
2. If any part of the query is unclear or lacks necessary information, ask for clarification before proceeding.
3. When providing code snippets, use the following format:
   ```language
   // Your code here
   ```
   Replace "language" with the appropriate programming language (e.g., python, javascript, java, etc.).

4. Structure your response as follows:
   a. Brief introduction or acknowledgment of the user's query
   b. Explanation of the solution or approach
   c. Code snippet(s) if applicable
   d. Additional explanations or considerations
   e. Conclusion or next steps

5. If you need to provide multiple code snippets or explanations, use appropriate headings and subheadings to organize your response.

6. Always double-check your response for accuracy and clarity before submitting it.

Now, process the following user query and provide your assistance:

<user_query>
{{USER_QUERY}}
</user_query>
    """

    try:
        response = client.messages.create(
            model=current_app.config['CLAUDE_MODEL'],
            max_tokens=current_app.config['MAX_TOKENS'],
            system=system_prompt,
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
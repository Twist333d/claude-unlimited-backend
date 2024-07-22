# Unleashed Claude: Unlimited Conversations with Claude AI

## Overview

Unleashed Claude is a web application that provides unlimited conversations with Anthropic's Claude AI, bypassing the limitations of the web interface. It offers real-time token usage tracking, cost estimation, and a user-friendly chat interface.

## Features

- Unlimited messaging with Claude AI
- Real-time token usage tracking
- Cost estimation for API usage
- Conversation history and retrieval
- User-friendly chat interface mimicking Claude's UI
- File upload capability
- Syntax highlighting and Markdown support
- Custom instructions support

## Tech Stack

- Backend: Flask (Python)
- Frontend: React
- Database: SQLite
- API: Anthropic's Claude API

## Prerequisites

- Python 3.7+
- Node.js 14+
- Anthropic API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/unleashed-claude.git
   cd unleashed-claude
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

4. Create a `.env` file in the `backend/app` directory and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the backend server:
   ```
   cd backend
   python -m app.run
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to use the application.

Alternatively, you can use the `run_app.py` script to start both the backend and frontend simultaneously:

```
python run_app.py
```

## Usage

1. Start a new conversation or select an existing one from the sidebar.
2. Type your message in the input box and press Enter or click the send button.
3. View Claude's response and continue the conversation.
4. Check the usage statistics in the right sidebar to monitor token usage and costs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Anthropic for providing the Claude AI API
- The Flask and React communities for their excellent frameworks and documentation
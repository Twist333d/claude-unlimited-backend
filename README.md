markdownCopy# Claude Unlimited Backend

This is the backend service for Claude Unlimited, an AI-powered chat application using Anthropic's Claude-3.5-Sonnet model.

## Project Structure
claude-unlimited-backend/
├── app/
│   ├── services/
│   │   ├── anthropic_service.py
│   │   └── chat_service.py
│   ├── utils/
│   │   ├── database.py
│   │   ├── logger.py
│   │   └── token_counter.py
│   ├── config.py
│   ├── routes.py
│   └── init.py
├── app.py
├── .env
├── .gitignore
├── Procfile
├── requirements.txt
└── README.md
Copy
## Setup

1. Clone the repository:
git clone https://github.com/yourusername/claude-unlimited-backend.git
cd claude-unlimited-backend
Copy
2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Copy
3. Install dependencies:
pip install -r requirements.txt
Copy
4. Set up environment variables:
Create a `.env` file in the root directory and add:
ANTHROPIC_API_KEY=your_api_key_here
FLASK_APP=app.py
FLASK_DEBUG=True
DATABASE_URL=sqlite:///chat_history.db
Copy
5. Initialize the database:
flask db upgrade
Copy
6. Run the application:
flask run
Copy
## Deployment to Heroku

1. Create a new Heroku app:
heroku create claude-unlimited-backend
Copy
2. Set environment variables:
heroku config:set ANTHROPIC_API_KEY=your_api_key_here
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_DEBUG=False
Copy
3. Deploy the application:
git push heroku main
Copy
4. Run database migrations:
heroku run flask db upgrade
Copy
## API Endpoints

- `POST /chat`: Send a message to Claude and receive a response.
- `GET /conversations`: Retrieve a list of all conversations.
- `GET /conversations/<id>/messages`: Retrieve messages for a specific conversation.
- `GET /usage`: Get usage statistics.

For detailed API documentation, refer to the `routes.py` file.

## Learn More

To learn more about the technologies used in this project, refer to:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Anthropic API Documentation](https://www.anthropic.com/product)
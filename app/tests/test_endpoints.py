import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variable for BASE_URL, defaulting to localhost if not set
BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

def get_test_token():
    response = requests.get(f"{BASE_URL}/generate_test_token")
    return response.json()['token']

def test_endpoints(token):
    headers = {"Authorization": f"Bearer {token}"}
    conversation_id = "c69abff2-a41a-46ff-8c77-e617141765a3"

    # Test /conversations (GET)
    response = requests.get(f"{BASE_URL}/conversations", headers=headers)
    print("GET /conversations:", response.status_code, response.json())

    # Test /conversations/{conversation_id}/messages (GET)
    response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/messages", headers=headers)
    print(f"GET /conversations/{conversation_id}/messages:", response.status_code, response.json())

    # Test /conversations/{conversation_id}/archive (POST)
    archive_data = {"archive": True}
    response = requests.post(f"{BASE_URL}/conversations/{conversation_id}/archive", headers=headers, json=archive_data)
    print(f"POST /conversations/{conversation_id}/archive:", response.status_code, response.json())

    # Test /chat (POST)
    chat_data = {
        "conversation_id": conversation_id,
        "message": "This is a test message"
    }
    response = requests.post(f"{BASE_URL}/chat", headers=headers, json=chat_data)
    print("POST /chat:", response.status_code, response.json())

    # Test /usage (GET)
    response = requests.get(f"{BASE_URL}/usage", headers=headers)
    print("GET /usage:", response.status_code, response.json())

    # Test /usage with conversation_id (GET)
    response = requests.get(f"{BASE_URL}/usage?conversation_id={conversation_id}", headers=headers)
    print(f"GET /usage with conversation_id:", response.status_code, response.json())

    # Test /user/settings (GET)
    response = requests.get(f"{BASE_URL}/user/settings", headers=headers)
    print("GET /user/settings:", response.status_code, response.json())

    # Test /user/settings (PUT)
    settings_data = {
        "custom_instructions": "Test custom instructions",
        "preferred_model": "Test model"
    }
    response = requests.put(f"{BASE_URL}/user/settings", headers=headers, json=settings_data)
    print("PUT /user/settings:", response.status_code, response.json())

if __name__ == "__main__":
    token = get_test_token()
    test_endpoints(token)
# app/tests/smoke_tests.py

import requests
import os
from flask import current_app
from app import create_app
from app.utils.auth import get_test_user_id

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

def get_test_token():
    app = create_app()
    with app.app_context():
        user_id = get_test_user_id()
        # Implement a function to generate a test token here
        # This is a placeholder and needs to be implemented based on your authentication system
        return "test_token"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200

def test_conversations_list():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/conversations", headers=headers)
    assert response.status_code == 200

def test_chat_functionality():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": "Hello, Claude!"}
    response = requests.post(f"{BASE_URL}/chat", headers=headers, json=data)
    assert response.status_code == 200
    assert "response" in response.json()

def test_usage_stats():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/usage", headers=headers)
    assert response.status_code == 200

def run_all_smoke_tests():
    test_health_check()
    test_conversations_list()
    test_chat_functionality()
    test_usage_stats()
    print("All smoke tests passed successfully!")

if __name__ == "__main__":
    run_all_smoke_tests()
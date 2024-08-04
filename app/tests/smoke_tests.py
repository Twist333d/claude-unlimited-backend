# app/tests/smoke_tests.py

import requests
import os
from datetime import datetime, timezone,  timedelta
from flask import current_app
from app import create_app
from app.utils.auth import get_user_id_from_request
import jwt

def get_test_token():
    app = create_app()
    with app.app_context():
        user_id = current_app.config['TEST_USER_ID']
        payload = {
            'sub': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        return jwt.encode(payload, current_app.config['SUPABASE_JWT_SECRET'], algorithm='HS256')

def run_smoke_tests():
    app = create_app()
    with app.app_context():
        base_url = current_app.config['APP_BASE_URL']
        token = get_test_token()

        headers = {"Authorization": f"Bearer {token}"}

        def test_health_check():
            response = requests.get(f"{base_url}/health")
            assert response.status_code == 200, "Health check failed"
            print("✅ Health check passed")

        def test_conversations_list():
            response = requests.get(f"{base_url}/conversations", headers=headers)
            assert response.status_code == 200, "Conversations list failed"
            print("✅ Conversations list check passed")

        def test_chat_functionality():
            data = {"message": "Hello, Claude!"}
            response = requests.post(f"{base_url}/chat", headers=headers, json=data)
            assert response.status_code == 200, "Chat functionality failed"
            assert "response" in response.json(), "Chat response is missing"
            print("✅ Chat functionality check passed")

        def test_usage_stats():
            response = requests.get(f"{base_url}/usage", headers=headers)
            assert response.status_code == 200, "Usage stats failed"
            print("✅ Usage stats check passed")

        def test_user_settings():
            response = requests.get(f"{base_url}/user/settings", headers=headers)
            assert response.status_code == 200, "User settings GET failed"
            print("✅ User settings GET check passed")

            data = {"custom_instructions": "Test instruction"}
            response = requests.put(f"{base_url}/user/settings", headers=headers, json=data)
            assert response.status_code == 200, "User settings PUT failed"
            print("✅ User settings PUT check passed")

        # Run all tests
        test_health_check()
        test_conversations_list()
        test_chat_functionality()
        test_usage_stats()
        test_user_settings()

        print("All smoke tests passed successfully!")

if __name__ == "__main__":
    run_smoke_tests()
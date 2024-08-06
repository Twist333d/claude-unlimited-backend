from .base_test import BaseTest

class TestAPI(BaseTest):
    def test_conversations(self, client, auth_headers):
        response = client.get('/conversations', headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_create_conversation(self, client, auth_headers):
        data = {
            "message": "This is a new conversation",
            "conversation_id": None  # This should trigger creation of a new conversation
        }
        response = client.post('/chat', headers=auth_headers, json=data)
        assert response.status_code == 200
        assert "conversation_id" in response.json
        assert "response" in response.json

    def test_conversation_messages(self, client, auth_headers, test_conversation):
        response = client.get(f'/conversations/{test_conversation["id"]}/messages', headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_chat(self, client, auth_headers, test_conversation):
        data = {
            "conversation_id": test_conversation["id"],
            "message": "This is a test message"
        }
        response = client.post('/chat', headers=auth_headers, json=data)
        assert response.status_code == 200
        assert "response" in response.json

    def test_usage(self, client, auth_headers):
        response = client.get('/usage', headers=auth_headers)
        assert response.status_code == 200
        assert "total_tokens" in response.json

    def test_user_settings(self, client, auth_headers):
        # Test GET
        response = client.get('/user/settings', headers=auth_headers)
        assert response.status_code == 200

        # Test PUT
        data = {
            "custom_instructions": "Test custom instructions",
            "preferred_model": "Test model"
        }
        response = client.put('/user/settings', headers=auth_headers, json=data)
        assert response.status_code == 200
        assert response.json["custom_instructions"] == data["custom_instructions"]

    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json["status"] == "healthy"
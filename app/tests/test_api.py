import pytest
from .base_test import BaseTest

class TestAPI(BaseTest):
    def test_list_user_conversations(self, client, base_url, app, test_user):
        headers = self.get_headers(app, test_user)
        response = client.get(f'{base_url}/conversations', headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_get_conversation_messages(self, client, base_url, test_conversation, app, test_user):
        headers = self.get_headers(app, test_user)
        response = client.get(f'{base_url}/conversations/{test_conversation["id"]}/messages', headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_chat_new_conversation(self, client, base_url, app, test_user):
        headers = self.get_headers(app, test_user)
        data = {"message": "This is a test message for a new conversation"}
        response = client.post(f'{base_url}/chat', headers=headers, json=data)
        assert response.status_code == 200
        assert 'response' in response.json
        assert 'conversation_id' in response.json

    def test_chat_existing_conversation(self, client, base_url, test_conversation, app, test_user):
        headers = self.get_headers(app, test_user)
        data = {
            "conversation_id": test_conversation["id"],
            "message": "This is a test message for an existing conversation"
        }
        response = client.post(f'{base_url}/chat', headers=headers, json=data)
        assert response.status_code == 200
        assert 'response' in response.json
        assert 'conversation_id' in response.json
        assert response.json['conversation_id'] == str(test_conversation["id"])

    def test_usage_stats(self, client, base_url, app, test_user):
        headers = self.get_headers(app, test_user)
        response = client.get(f'{base_url}/usage', headers=headers)
        assert response.status_code == 200
        assert 'total_tokens' in response.json
        assert 'total_cost' in response.json
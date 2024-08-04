import pytest
from .base_test import BaseTest

class TestAPI(BaseTest):
    def test_generate_test_token(self, client):
        response = client.get('/generate_test_token')
        assert response.status_code == 200
        assert 'token' in response.json

    def test_conversations(self, client, base_url):
        headers = self.get_headers(client)
        response = client.get(f'{base_url}/conversations', headers=headers)
        assert response.status_code == 200

    def test_conversation_messages(self, client, base_url):
        headers = self.get_headers(client)
        conversation_id = "c69abff2-a41a-46ff-8c77-e617141765a3"
        response = client.get(f'{base_url}/conversations/{conversation_id}/messages', headers=headers)
        assert response.status_code == 200

    def test_archive_conversation(self, client, base_url):
        headers = self.get_headers(client)
        conversation_id = "c69abff2-a41a-46ff-8c77-e617141765a3"
        data = {"archive": True}
        response = client.post(f'{base_url}/conversations/{conversation_id}/archive', headers=headers, json=data)
        assert response.status_code == 200

    def test_chat(self, client, base_url):
        headers = self.get_headers(client)
        data = {
            "conversation_id": "c69abff2-a41a-46ff-8c77-e617141765a3",
            "message": "This is a test message"
        }
        response = client.post(f'{base_url}/chat', headers=headers, json=data)
        assert response.status_code == 200

    def test_usage(self, client, base_url):
        headers = self.get_headers(client)
        response = client.get(f'{base_url}/usage', headers=headers)
        assert response.status_code == 200

    def test_user_settings(self, client, base_url):
        headers = self.get_headers(client)

        # Test GET
        response = client.get(f'{base_url}/user/settings', headers=headers)
        assert response.status_code == 200

        # Test PUT
        data = {
            "custom_instructions": "Test custom instructions",
            "preferred_model": "Test model"
        }
        response = client.put(f'{base_url}/user/settings', headers=headers, json=data)
        assert response.status_code == 200
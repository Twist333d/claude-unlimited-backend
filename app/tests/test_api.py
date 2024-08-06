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

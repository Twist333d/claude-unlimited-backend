import os
import pytest
from app import create_app
from app.config import get_config

class BaseTest:
    @pytest.fixture(scope='class')
    def app(self):
        app = create_app(get_config())
        return app

    @pytest.fixture(scope='class')
    def client(self, app):
        return app.test_client()

    @pytest.fixture(scope='class')
    def base_url(self, app):
        return app.config['BASE_URL']

    @pytest.fixture(scope='class')
    def test_user_id(self, app):
        return app.config['TEST_USER_ID']

    @pytest.fixture(scope='class')
    def test_conversation_id(self, app):
        return app.config['TEST_CONVERSATION_ID']

    def get_headers(self, client):
        response = client.get('/generate_test_token')
        token = response.json['token']
        return {"Authorization": f"Bearer {token}"}
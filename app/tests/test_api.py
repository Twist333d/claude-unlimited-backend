import pytest
import requests
from app import create_app
from app.config import TestConfig


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client


def test_generate_test_token(client):
    response = client.get('/generate_test_token')
    assert response.status_code == 200
    assert 'token' in response.json


def test_conversations(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/conversations', headers=headers)
    assert response.status_code == 200


def test_conversation_messages(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}
    conversation_id = "c69abff2-a41a-46ff-8c77-e617141765a3"
    response = client.get(f'/conversations/{conversation_id}/messages', headers=headers)
    assert response.status_code == 200


def test_archive_conversation(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}
    conversation_id = "c69abff2-a41a-46ff-8c77-e617141765a3"
    data = {"archive": True}
    response = client.post(f'/conversations/{conversation_id}/archive', headers=headers, json=data)
    assert response.status_code == 200


def test_chat(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "conversation_id": "c69abff2-a41a-46ff-8c77-e617141765a3",
        "message": "This is a test message"
    }
    response = client.post('/chat', headers=headers, json=data)
    assert response.status_code == 200


def test_usage(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/usage', headers=headers)
    assert response.status_code == 200


def test_user_settings(client):
    token = client.get('/generate_test_token').json['token']
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET
    response = client.get('/user/settings', headers=headers)
    assert response.status_code == 200

    # Test PUT
    data = {
        "custom_instructions": "Test custom instructions",
        "preferred_model": "Test model"
    }
    response = client.put('/user/settings', headers=headers, json=data)
    assert response.status_code == 200
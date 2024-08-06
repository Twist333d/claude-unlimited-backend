import pytest
from app import create_app
from app.config import get_config

class BaseTest:
    @pytest.fixture(scope='class')
    def app(self):
        app = create_app(get_config('testing'))
        return app

    @pytest.fixture(scope='class')
    def client(self, app):
        return app.test_client()

    @pytest.fixture(scope='class')
    def supabase_client(self, app):
        return app.supabase

    @pytest.fixture(scope='function')
    def anonymous_token(self, supabase_client):
        response = supabase_client.auth.sign_in_anonymously()
        yield response.session.access_token
        # Clean up: sign out after the test
        supabase_client.auth.sign_out({"scope": "global"})

    @pytest.fixture(scope='function')
    def auth_headers(self, anonymous_token):
        return {"Authorization": f"Bearer {anonymous_token}"}

    @pytest.fixture(scope='function')
    def test_conversation(self, supabase_client, anonymous_token):
        user = supabase_client.auth.get_user(anonymous_token)
        conversation = supabase_client.table('conversations').insert({
            "user_id": user.user.id,
            "title": "Test Conversation"
        }).execute()
        yield conversation.data[0]
        # Clean up: delete usage_stats, messages, and then the conversation after the test
        supabase_client.table('usage_stats').delete().eq('conversation_id', conversation.data[0]['id']).execute()
        supabase_client.table('messages').delete().eq('conversation_id', conversation.data[0]['id']).execute()
        supabase_client.table('conversations').delete().eq('id', conversation.data[0]['id']).execute()
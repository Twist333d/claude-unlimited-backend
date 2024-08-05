import pytest
import uuid
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
        return app.config['APP_BASE_URL']

    @pytest.fixture(scope='class')
    def test_user(self, app):
        # Create a test user dynamically
        unique_id = uuid.uuid4()
        user = app.supabase.auth.sign_up({
            'email': f'testuser_{unique_id}@example.com',
            'password': 'testpassword123'
        })
        yield user.user
        # We don't delete the user, as we don't have admin privileges in local development

    @pytest.fixture(scope='class')
    def test_conversation(self, app, test_user):
        # Create a test conversation dynamically
        conversation = app.supabase.table('conversations').insert({
            'user_id': test_user.id,
            'title': 'Test Conversation'
        }).execute()
        yield conversation.data[0]
        # Clean up: delete messages first, then the conversation
        app.supabase.table('messages').delete().eq('conversation_id', conversation.data[0]['id']).execute()
        app.supabase.table('conversations').delete().eq('id', conversation.data[0]['id']).execute()

    def get_headers(self, app, test_user):
        session = app.supabase.auth.sign_in_with_password({
            'email': test_user.email,
            'password': 'testpassword123'
        })
        return {"Authorization": f"Bearer {session.session.access_token}"}
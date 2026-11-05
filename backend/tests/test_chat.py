from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.deps import get_chat_service
from app.main import app
from app.services.chat_service import ChatService

client = TestClient(app)


class FakeClaude:
    '''Pretends to be the Anthropic client: returns a fixed answer.'''

    def __init__(self):
        self.messages = self

    def create(self, **kwargs):
        return SimpleNamespace(
            content=[SimpleNamespace(type='text', text='Hello from the fake!')],
            usage=SimpleNamespace(input_tokens=10, output_tokens=5),
        )


def test_chat_with_fake_llm():
    app.dependency_overrides[get_chat_service] = lambda: ChatService(llm=FakeClaude())
    try:
        r = client.post('/v1/chat', json={'message': 'Hi'})
        assert r.status_code == 200
        assert r.json()['answer'] == 'Hello from the fake!'
    finally:
        app.dependency_overrides.clear()


def test_empty_message_rejected():
    r = client.post('/v1/chat', json={'message': ''})
    assert r.status_code == 422
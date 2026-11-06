import httpx

from intelligent_hpc_operations.ai_assistant.api_client import OpenAICompatibleClient
from intelligent_hpc_operations.ai_assistant.config import Settings


def test_client_sends_tool_payload_and_auth_header():
    observed = {}

    def handler(request):
        observed["url"] = str(request.url)
        observed["authorization"] = request.headers.get("authorization")
        observed["payload"] = request.read().decode()
        return httpx.Response(
            200,
            json={"choices": [{"message": {"role": "assistant", "content": "hello"}}]},
        )

    settings = Settings(
        base_url="http://test.local/v1", model="test-model", api_key="test-key"
    )
    with OpenAICompatibleClient(settings, transport=httpx.MockTransport(handler)) as client:
        response = client.complete([{"role": "user", "content": "hi"}], [])

    assert response["content"] == "hello"
    assert observed["url"] == "http://test.local/v1/chat/completions"
    assert observed["authorization"] == "Bearer test-key"
    assert '"model":"test-model"' in observed["payload"]

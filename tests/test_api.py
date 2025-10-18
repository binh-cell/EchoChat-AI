"""Integration tests for the chatbot HTTP API."""

import json

from chatbot import ChatBot, _build_environ, create_app


def _invoke(app, body: dict) -> tuple[str, dict[str, str], dict]:
    captured: dict[str, str | list[tuple[str, str]]] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        captured["status"] = status
        captured["headers"] = headers

    environ = _build_environ("POST", "/chat", json.dumps(body).encode("utf-8"))
    payload = b"".join(app(environ, start_response))
    headers = dict(captured.get("headers", []))
    return captured.get("status", ""), headers, json.loads(payload.decode("utf-8"))


def test_chat_endpoint_returns_bot_reply():
    app = create_app(ChatBot([]))

    status, headers, data = _invoke(app, {"message": "hello"})

    assert status.startswith("200")
    assert headers["Content-Type"] == "application/json"
    assert data["reply"].startswith("Hello!")


def test_empty_message_returns_validation_error():
    app = create_app(ChatBot([]))

    status, _, data = _invoke(app, {"message": "   "})

    assert status.startswith("422")
    assert data["detail"] == "message must not be empty"

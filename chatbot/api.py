"""Minimal WSGI application exposing the EchoChat chatbot over HTTP."""

from __future__ import annotations

import json
from io import BytesIO
from typing import Callable, Iterable
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from .bot import ChatBot

StartResponse = Callable[[str, list[tuple[str, str]]], None]
Environ = dict[str, object]


def _read_body(environ: Environ) -> str:
    try:
        length = int(environ.get("CONTENT_LENGTH", "0"))
    except (TypeError, ValueError):
        length = 0

    body_bytes = environ.get("wsgi.input")
    if not hasattr(body_bytes, "read"):
        return ""

    return body_bytes.read(length).decode("utf-8")


def create_app(bot: ChatBot | None = None) -> Callable[[Environ, StartResponse], Iterable[bytes]]:
    """Create a simple WSGI application backed by ``bot``."""

    chatbot = bot or ChatBot()

    def application(environ: Environ, start_response: StartResponse) -> Iterable[bytes]:
        setup_testing_defaults(environ)

        method = environ.get("REQUEST_METHOD")
        path = environ.get("PATH_INFO")

        if method != "POST" or path != "/chat":
            start_response("404 Not Found", [("Content-Type", "application/json")])
            return [json.dumps({"detail": "Not found"}).encode("utf-8")]

        body_text = _read_body(environ)

        try:
            payload = json.loads(body_text or "{}")
        except json.JSONDecodeError:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"detail": "Invalid JSON"}).encode("utf-8")]

        message = str(payload.get("message", "")).strip()
        if not message:
            start_response("422 Unprocessable Entity", [("Content-Type", "application/json")])
            return [json.dumps({"detail": "message must not be empty"}).encode("utf-8")]

        reply = chatbot.reply(message)
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps({"reply": reply}).encode("utf-8")]

    return application


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the chatbot API using Python's built-in WSGI server."""

    app = create_app()
    with make_server(host, port, app) as httpd:
        print(f"Serving EchoChat API on http://{host}:{port}")
        httpd.serve_forever()


def _build_environ(method: str, path: str, body: bytes | None = None) -> Environ:
    """Utility for tests to craft a WSGI ``environ``."""

    environ: Environ = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = method
    environ["PATH_INFO"] = path
    environ["CONTENT_LENGTH"] = str(len(body or b""))
    environ["CONTENT_TYPE"] = "application/json"
    environ["wsgi.input"] = BytesIO(body or b"")
    return environ


__all__ = ["create_app", "run", "_build_environ"]

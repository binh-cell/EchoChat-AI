# EchoChat AI

EchoChat AI is a lightweight, fully offline chatbot that runs in the terminal. It
uses a small collection of keyword-driven rules to craft helpful and friendly
responses, making it a perfect starting point for experimentation.

## Getting started

1. Ensure you have Python 3.11+ installed.
2. Install the (optional) development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Pick an interface:

   - **Terminal chat**

     ```bash
     python main.py
     ```

     Type your message and press Enter. Say `bye` when you are done.

   - **HTTP API**

     ```bash
     python -m chatbot.api
     ```

     Once running, send a JSON payload to `POST /chat`:

     ```bash
     curl -X POST http://127.0.0.1:8000/chat \
       -H "Content-Type: application/json" \
       -d '{"message": "hello there"}'
     ```

     The API responds with a JSON object containing the bot's reply.

## Running tests

The project ships with a small pytest suite that exercises the core chatbot
logic. Run the tests with:

```bash
pytest
```

## Project structure

```
.
├── chatbot/          # Chatbot logic and HTTP API
├── main.py           # Command-line interface entrypoint
└── tests/            # Unit tests for the chatbot
```

Feel free to add more response rules, hook the bot into messaging platforms, or
wrap it in a web UI to keep evolving EchoChat AI.

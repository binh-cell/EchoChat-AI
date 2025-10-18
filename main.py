"""Command-line interface for chatting with the EchoChat bot."""

from __future__ import annotations

import sys

from chatbot import ChatBot


def run() -> None:
    """Start a conversation with the chatbot via standard input/output."""

    bot = ChatBot()
    print("Welcome to EchoChat! Type 'bye' to end the conversation.\n")

    while True:
        try:
            message = input("You: ")
        except EOFError:
            print("\nGoodbye!")
            break

        reply = bot.reply(message)
        print(f"EchoChat: {reply}")

        if reply == bot._fallbacks["farewell"]:  # pragma: no cover - simple exit condition
            break


if __name__ == "__main__":  # pragma: no cover
    run()

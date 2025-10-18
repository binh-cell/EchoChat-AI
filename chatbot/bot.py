"""Core conversational logic for the EchoChat chatbot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence


@dataclass
class ResponseRule:
    """Mapping of trigger keywords to canned responses."""

    keywords: Sequence[str]
    response: str

    def matches(self, message: str) -> bool:
        """Return ``True`` when all keywords are present in ``message``.

        The comparison is case-insensitive and ignores punctuation by working on a
        normalized, lower-case representation of the message.
        """

        normalized = _normalize(message)
        return all(keyword in normalized for keyword in self.keywords)


def _normalize(message: str) -> str:
    """Normalize ``message`` for keyword matching."""

    return " ".join(message.lower().split())


class ChatBot:
    """Simple conversational agent powered by keyword rules and fallbacks."""

    def __init__(self, rules: Iterable[ResponseRule] | None = None) -> None:
        self._rules: List[ResponseRule] = list(rules or _default_rules())
        self._fallbacks: Dict[str, str] = {
            "greeting": "Hello! I'm EchoChat, your friendly assistant. How can I help today?",
            "unknown": "I'm not sure how to respond to that yet, but I'm learning every day!",
            "farewell": "Thanks for chatting with EchoChat. Talk soon!",
        }

    def reply(self, message: str) -> str:
        """Generate a response for ``message``."""

        normalized = _normalize(message)
        if not normalized:
            return "Please say something so I can respond."

        if any(word in normalized for word in ("bye", "goodbye", "see you")):
            return self._fallbacks["farewell"]

        if any(word in normalized for word in ("hi", "hello", "hey")):
            return self._fallbacks["greeting"]

        for rule in self._rules:
            if rule.matches(normalized):
                return rule.response

        return self._fallbacks["unknown"]


def _default_rules() -> List[ResponseRule]:
    """Return the default set of keyword-driven response rules."""

    return [
        ResponseRule(("help",), "Sure! Describe what you need help with and I'll do my best."),
        ResponseRule(("your", "name"), "I'm EchoChat, a tiny yet mighty chatbot."),
        ResponseRule(
            ("weather",),
            "I can't fetch live weather yet, but checking your favorite weather app should do the trick!",
        ),
        ResponseRule(("creator",), "I was crafted just now with love and Python."),
        ResponseRule(
            ("thanks",),
            "You're very welcome! If you have more questions, just let me know.",
        ),
    ]

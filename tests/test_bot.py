"""Tests for the EchoChat chatbot logic."""

from chatbot import ChatBot, ResponseRule


def test_greeting_detection():
    bot = ChatBot([])
    assert "friendly assistant" in bot.reply("hello there")


def test_unknown_response_when_no_rules_match():
    bot = ChatBot([])
    assert "I'm not sure" in bot.reply("what is the capital of mars?")


def test_custom_rules_take_priority():
    rules = [ResponseRule(("mars",), "Mars is the red planet!")]
    bot = ChatBot(rules)
    assert bot.reply("tell me about mars") == "Mars is the red planet!"


def test_empty_input_prompts_user():
    bot = ChatBot([])
    assert bot.reply("   ") == "Please say something so I can respond."

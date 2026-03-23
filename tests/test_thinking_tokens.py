"""Tests for thinking-token stripping and APIClient postprocessing."""
import pytest
from call_api import strip_thinking_tokens, APIConfig


class TestStripThinkingTokens:
    def test_single_block(self):
        text = "<think>reasoning here</think>\nAnswer: 42"
        assert strip_thinking_tokens(text) == "Answer: 42"

    def test_multiple_blocks(self):
        text = "<think>first</think>middle<think>second</think>end"
        assert strip_thinking_tokens(text) == "middleend"

    def test_multiline_block(self):
        text = "<think>\nline1\nline2\nline3\n</think>\nResult"
        assert strip_thinking_tokens(text) == "Result"

    def test_no_thinking_tokens(self):
        text = "Just a normal response"
        assert strip_thinking_tokens(text) == "Just a normal response"

    def test_empty_string(self):
        assert strip_thinking_tokens("") == ""

    def test_only_thinking(self):
        text = "<think>everything is thinking</think>"
        assert strip_thinking_tokens(text) == ""

    def test_leading_whitespace_stripped(self):
        text = "<think>stuff</think>   \n  actual content"
        result = strip_thinking_tokens(text)
        assert result == "actual content"

    def test_nested_angle_brackets(self):
        """Thinking block containing < > characters inside."""
        text = "<think>if x < 3 and y > 5 then...</think>\nAnswer"
        assert strip_thinking_tokens(text) == "Answer"

    def test_real_world_qwen_output(self):
        text = (
            "<think>\nOkay, let me analyze this problem step by step.\n"
            "First, I need to identify the facts.\n"
            "Then I'll create the rules.\n"
            "</think>\n"
            "```facts\nis_cold(\"Bob\", True)\n```\n"
            "```rules\nrule1\n```\n"
            "```query\nfacts.is_cold(\"Bob\", True)\n```"
        )
        result = strip_thinking_tokens(text)
        assert result.startswith("```facts")
        assert "<think>" not in result


class TestAPIConfigStripThinking:
    def test_default_is_true(self):
        config = APIConfig(model_name="test")
        assert config.strip_thinking is True

    def test_can_disable(self):
        config = APIConfig(model_name="test", strip_thinking=False)
        assert config.strip_thinking is False

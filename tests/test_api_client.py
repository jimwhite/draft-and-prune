"""Tests for APIClient._postprocess_response and metadata storage."""
import pytest
from call_api import APIConfig, OpenAICompatibleClient


class TestPostprocessResponse:
    """Test the _postprocess_response pipeline on a concrete client."""

    def _make_client(self, strip_thinking: bool = True) -> OpenAICompatibleClient:
        config = APIConfig(
            model_name="test-model",
            strip_thinking=strip_thinking,
        )
        return OpenAICompatibleClient(config, api_key="fake", base_url="http://localhost:1")

    def test_strips_thinking_when_enabled(self):
        client = self._make_client(strip_thinking=True)
        result = client._postprocess_response("<think>blah</think>\nAnswer")
        assert result == "Answer"
        assert client.last_call_metadata["raw_response"] == "<think>blah</think>\nAnswer"

    def test_preserves_when_disabled(self):
        client = self._make_client(strip_thinking=False)
        result = client._postprocess_response("<think>blah</think>\nAnswer")
        assert result == "<think>blah</think>\nAnswer"
        assert client.last_call_metadata["raw_response"] == "<think>blah</think>\nAnswer"

    def test_no_thinking_tokens_passthrough(self):
        client = self._make_client(strip_thinking=True)
        result = client._postprocess_response("clean response")
        assert result == "clean response"

    def test_empty_string(self):
        client = self._make_client(strip_thinking=True)
        result = client._postprocess_response("")
        assert result == ""


class TestMetadataNotClobbered:
    """Verify that _set_last_call_usage and _set_last_call_timing
    don't clobber prompt and raw_response keys."""

    def _make_client(self) -> OpenAICompatibleClient:
        config = APIConfig(model_name="test-model")
        return OpenAICompatibleClient(config, api_key="fake", base_url="http://localhost:1")

    def test_prompt_survives_usage_and_timing(self):
        client = self._make_client()
        client._clear_last_call_metadata()
        client._set_last_call_prompt("my prompt")
        client._postprocess_response("my response")
        client._set_last_call_timing(1.5, 2)
        client._set_last_call_usage(None)

        meta = client.get_last_call_metadata()
        assert meta["prompt"] == "my prompt"
        assert meta["raw_response"] == "my response"
        assert meta["timing"]["api_time_only_sec"] == 1.5
        assert meta["usage"] is None

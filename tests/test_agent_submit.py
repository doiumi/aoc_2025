import json
from pathlib import Path

import pytest

from agent.config import AgentConfig
from agent.submit import RateLimitError, SubmitResult, submit_answer


class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


def test_submit_respects_rate_limit(tmp_path: Path, monkeypatch):
    config = AgentConfig(session_cookie="dummy")

    def fake_post(day, part, answer, config):
        return DummyResponse("That's the right answer!")

    monkeypatch.setattr("agent.submit._post_answer", fake_post)

    first = submit_answer(1, 1, "123", config, base_dir=tmp_path, now=0)
    assert isinstance(first, SubmitResult)
    assert first.status == "correct"

    with pytest.raises(RateLimitError):
        submit_answer(1, 1, "123", config, base_dir=tmp_path, now=10)

    # After cooldown
    second = submit_answer(1, 1, "123", config, base_dir=tmp_path, now=70)
    assert second.status == "correct"

    state = json.loads((tmp_path / ".agent_state.json").read_text())
    assert "1-1" in state

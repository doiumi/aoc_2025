import types
from pathlib import Path

import pytest

from agent.config import AgentConfig
from agent.errors import FetchError, LockedDayError
from agent import fetch


class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


@pytest.fixture
def config():
    return AgentConfig(session_cookie="dummy")


def test_fetch_puzzle_uses_cache(tmp_path: Path, config, monkeypatch):
    cache_file = tmp_path / "puzzles" / "day_01.html"
    cache_file.parent.mkdir(parents=True)
    cache_file.write_text("cached puzzle")

    called = False

    def fail_get(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("Should not reach network when cache exists")

    monkeypatch.setattr(fetch, "_aoc_get", fail_get)

    result = fetch.fetch_puzzle(1, config, base_dir=tmp_path)
    assert result.source == "cache"
    assert result.content == "cached puzzle"
    assert called is False


def test_fetch_input_network_writes_cache(tmp_path: Path, config, monkeypatch):
    def fake_get(url, config):
        return DummyResponse("42\n", status_code=200)

    monkeypatch.setattr(fetch, "_aoc_get", fake_get)

    result = fetch.fetch_input(2, config, base_dir=tmp_path, force=True)
    assert result.source == "network"
    assert result.content == "42"
    assert result.path.exists()
    assert result.path.read_text() == "42"


def test_locked_day_detected(tmp_path: Path, config, monkeypatch):
    def locked_get(url, config):
        return DummyResponse("not found", status_code=404)

    monkeypatch.setattr(fetch, "_aoc_get", locked_get)

    with pytest.raises(LockedDayError):
        fetch.fetch_puzzle(25, config, base_dir=tmp_path, force=True)


def test_non_200_raises(tmp_path: Path, config, monkeypatch):
    def bad_get(url, config):
        return DummyResponse("error", status_code=500)

    monkeypatch.setattr(fetch, "_aoc_get", bad_get)

    with pytest.raises(FetchError):
        fetch.fetch_input(3, config, base_dir=tmp_path, force=True)

"""
Fetching utilities for AoC puzzles and inputs with simple caching and locked-day detection.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

import requests

from agent import YEAR
from agent.config import AgentConfig
from agent.errors import FetchError, LockedDayError

Source = Literal["cache", "network"]

USER_AGENT = "aoc-agent/0.1 (+https://github.com/doiumi/aoc_2025)"


@dataclass
class FetchResult:
    content: str
    path: Path
    source: Source
    status_code: int


def _aoc_get(url: str, config: AgentConfig) -> requests.Response:
    cookies = {"session": config.session_cookie}
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, cookies=cookies, headers=headers, timeout=15)
    return response


def _handle_response(response: requests.Response, day: int) -> str:
    if response.status_code == 404:
        raise LockedDayError(f"Day {day} is not available yet (404).")
    if response.status_code == 400:
        raise FetchError("Bad request when fetching AoC content.")
    if response.status_code != 200:
        raise FetchError(f"Unexpected status {response.status_code} from AoC.")

    # Do not rely on heuristic text checks; available pages mention "unlock" for part 2.
    return response.text


def fetch_puzzle(day: int, config: AgentConfig, *, base_dir: Optional[Path] = None, force: bool = False) -> FetchResult:
    base = base_dir or Path(__file__).resolve().parent.parent
    cache_path = base / "puzzles" / f"day_{day:02d}.html"
    if cache_path.exists() and not force:
        return FetchResult(content=cache_path.read_text(), path=cache_path, source="cache", status_code=200)

    url = f"https://adventofcode.com/{config.year}/day/{day}"
    response = _aoc_get(url, config)
    text = _handle_response(response, day)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(text)
    return FetchResult(content=text, path=cache_path, source="network", status_code=response.status_code)


def fetch_input(day: int, config: AgentConfig, *, base_dir: Optional[Path] = None, force: bool = False) -> FetchResult:
    base = base_dir or Path(__file__).resolve().parent.parent
    cache_path = base / "inputs" / f"day_{day:02d}.txt"
    if cache_path.exists() and not force:
        return FetchResult(content=cache_path.read_text().strip(), path=cache_path, source="cache", status_code=200)

    url = f"https://adventofcode.com/{config.year}/day/{day}/input"
    response = _aoc_get(url, config)
    text = _handle_response(response, day)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(text.strip())
    return FetchResult(content=text.strip(), path=cache_path, source="network", status_code=response.status_code)


def polite_sleep(delay_seconds: float = 1.0) -> None:
    """Small delay helper to avoid rapid-fire requests."""
    time.sleep(delay_seconds)

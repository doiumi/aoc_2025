"""
Submission utilities with simple rate limiting.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import requests

from agent import YEAR
from agent.config import AgentConfig
from agent.errors import FetchError

STATE_FILE = ".agent_state.json"
SUBMIT_COOLDOWN_SECONDS = 60
USER_AGENT = "aoc-agent/0.1 (+https://github.com/doiumi/aoc_2025)"


class SubmitError(FetchError):
    """Raised when submission fails."""


class RateLimitError(SubmitError):
    """Raised when submissions are too frequent."""


@dataclass
class SubmitResult:
    status: str
    message: str
    path: Path
    response_status: int


def _state_path(base_dir: Path | None = None) -> Path:
    base = base_dir or Path(__file__).resolve().parent.parent
    return base / STATE_FILE


def _load_state(path: Path) -> Dict[str, float]:
    if not path.exists():
        return {}
    return json.loads(path.read_text() or "{}")


def _save_state(path: Path, state: Dict[str, float]) -> None:
    path.write_text(json.dumps(state, indent=2))


def _post_answer(day: int, part: int, answer: str, config: AgentConfig) -> requests.Response:
    url = f"https://adventofcode.com/{config.year}/day/{day}/answer"
    cookies = {"session": config.session_cookie}
    headers = {"User-Agent": USER_AGENT}
    data = {"level": part, "answer": answer}
    return requests.post(url, cookies=cookies, headers=headers, data=data, timeout=15)


def submit_answer(
    day: int,
    part: int,
    answer: str,
    config: AgentConfig,
    *,
    base_dir: Optional[Path] = None,
    now: Optional[float] = None,
) -> SubmitResult:
    state_path = _state_path(base_dir)
    state = _load_state(state_path)
    key = f"{day}-{part}"
    current_time = now if now is not None else time.time()
    last = state.get(key)
    if last is not None and current_time - last < SUBMIT_COOLDOWN_SECONDS:
        raise RateLimitError(
            f"Submission too soon. Please wait {int(SUBMIT_COOLDOWN_SECONDS - (current_time - last))} seconds."
        )

    response = _post_answer(day, part, answer, config)
    text = response.text.lower()

    if response.status_code != 200:
        raise SubmitError(f"Unexpected status {response.status_code} from AoC submit.")

    if "right answer" in text:
        status = "correct"
    elif "not the right answer" in text:
        status = "incorrect"
    elif "did you already complete it" in text:
        status = "already_solved"
    else:
        status = "unknown"

    state[key] = current_time
    _save_state(state_path, state)

    return SubmitResult(status=status, message=response.text.strip(), path=state_path, response_status=response.status_code)

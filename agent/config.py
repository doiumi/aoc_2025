"""
Configuration helpers for the AoC agent.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from agent import YEAR


class ConfigError(Exception):
    """Raised when agent configuration is invalid or missing."""


SESSION_FILE = ".aoc_session"


@dataclass
class AgentConfig:
    session_cookie: str
    year: int = YEAR


def load_config() -> AgentConfig:
    """
    Load configuration from environment variables.

    Expected:
    - AOC_SESSION: Advent of Code session cookie value.
    Or fallback to a local .aoc_session file (root of repo).
    """
    session = os.getenv("AOC_SESSION")
    if not session:
        session_path = os.path.join(os.getcwd(), SESSION_FILE)
        if os.path.exists(session_path):
            session = open(session_path, "r", encoding="utf-8").read().strip()
    if not session:
        raise ConfigError("Missing AOC_SESSION (env var) and .aoc_session file for authentication.")
    return AgentConfig(session_cookie=session, year=YEAR)


def validate_day(day: int) -> int:
    """Validate day number for the configured year."""
    if day < 1 or day > 25:
        raise ConfigError(f"Day must be between 1 and 25, got {day}.")
    return day


def validate_part(part: int) -> int:
    """Validate puzzle part number."""
    if part not in (1, 2):
        raise ConfigError(f"Part must be 1 or 2, got {part}.")
    return part

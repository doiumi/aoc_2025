"""
Scaffolding utilities for new day solutions and tests.
"""

from __future__ import annotations

from pathlib import Path

from agent.config import ConfigError

SOLUTION_TEMPLATE = '''"""Day {day:02d} solution."""

from __future__ import annotations


def solve_part1(input_text: str) -> int:
    """Solve Part 1."""
    raise NotImplementedError("Day {day:02d} Part 1 not implemented yet")


def solve_part2(input_text: str) -> int:
    """Solve Part 2."""
    raise NotImplementedError("Day {day:02d} Part 2 not implemented yet")
'''

TEST_TEMPLATE = """import pytest

from aoc_2025.solutions import day_{day:02d}


def test_part1_placeholder():
    with pytest.raises(NotImplementedError):
        day_{day:02d}.solve_part1(\"test\")


def test_part2_placeholder():
    with pytest.raises(NotImplementedError):
        day_{day:02d}.solve_part2(\"test\")
"""


def scaffold_day(day: int, base_dir: Path | None = None) -> tuple[Path, Path]:
    if day < 1 or day > 25:
        raise ConfigError(f"Day must be between 1 and 25, got {day}.")

    base = base_dir or Path(__file__).resolve().parent.parent
    sol_dir = base / "aoc_2025" / "solutions"
    tests_dir = base / "tests"

    sol_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    sol_path = sol_dir / f"day_{day:02d}.py"
    test_path = tests_dir / f"test_day_{day:02d}.py"

    if not sol_path.exists():
        sol_path.write_text(SOLUTION_TEMPLATE.format(day=day))
    if not test_path.exists():
        test_path.write_text(TEST_TEMPLATE.format(day=day))

    return sol_path, test_path

"""
Solver runner utilities for AoC solutions.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Callable, Tuple

from agent.config import ConfigError


def default_input_path(day: int) -> Path:
    return Path(__file__).resolve().parent.parent / "inputs" / f"day_{day:02d}.txt"


def load_solver(day: int):
    module_name = f"aoc_2025.solutions.day_{day:02d}"
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as exc:
        raise ConfigError(f"No solver found for day {day:02d}.") from exc

    solve_part1 = getattr(module, "solve_part1", None)
    solve_part2 = getattr(module, "solve_part2", None)
    if not solve_part1 or not solve_part2:
        raise ConfigError(f"Solver for day {day:02d} is missing solve_part1/solve_part2.")
    return solve_part1, solve_part2


def run_solver(day: int, part: int, *, input_path: Path | None = None, input_text: str | None = None):
    path = input_path or default_input_path(day)
    if input_text is None:
        if not path.exists():
            raise ConfigError(f"Input file not found: {path}")
        input_text = path.read_text().strip()

    solve_part1, solve_part2 = load_solver(day)
    part1_result = solve_part1(input_text)
    if part == 1:
        return part1_result

    part2_result = solve_part2(input_text)
    return part1_result, part2_result

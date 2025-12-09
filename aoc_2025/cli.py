"""
Command-line runner for Advent of Code 2025 solutions.
"""

from __future__ import annotations

import argparse
from importlib import import_module
from pathlib import Path
from typing import Callable, Tuple

SolverPair = Tuple[Callable[[str], int], Callable[[str], int]]


def load_solvers(day: int) -> SolverPair:
    """Dynamically load solvers for a given day."""
    module_name = f"aoc_2025.solutions.day_{day:02d}"
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as exc:
        raise SystemExit(f"No solutions found for day {day:02d}") from exc

    try:
        return module.solve_part1, module.solve_part2
    except AttributeError as exc:
        raise SystemExit(f"Solutions for day {day:02d} are incomplete.") from exc


def default_input_path(day: int) -> Path:
    """Return the default input path for a given day."""
    return Path(__file__).resolve().parent.parent / "inputs" / f"day_{day:02d}.txt"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Advent of Code 2025 solutions.")
    parser.add_argument("--day", type=int, required=True, help="Day number (e.g., 1, 2).")
    parser.add_argument("--part", type=int, choices=[1, 2], required=True, help="Puzzle part (1 or 2).")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to input file. Defaults to inputs/day_##.txt",
    )
    args = parser.parse_args(argv)

    solve_part1, solve_part2 = load_solvers(args.day)
    solver = solve_part1 if args.part == 1 else solve_part2

    input_path = args.input or default_input_path(args.day)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    input_text = input_path.read_text().strip()
    result = solver(input_text)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Day 2: Gift Shop - Invalid Product ID Finder

Part 1: Invalid IDs are numbers made of a digit sequence repeated exactly twice.
Part 2: Invalid IDs are numbers made of a digit sequence repeated at least twice.
"""

from __future__ import annotations

from typing import Callable, List

from aoc_2025.utils import has_repeated_pattern, parse_ranges


def is_invalid_part1(num: int) -> bool:
    """Check if a number is an invalid ID under Part 1 rules (exactly two repeats)."""
    return has_repeated_pattern(num, exact_repeats=2)


def is_invalid_part2(num: int) -> bool:
    """Check if a number is an invalid ID under Part 2 rules (at least two repeats)."""
    return has_repeated_pattern(num, min_repeats=2)


def find_invalid_ids_in_range(start: int, end: int, check_fn: Callable[[int], bool]) -> List[int]:
    """Find all invalid IDs within a range (inclusive)."""
    return [num for num in range(start, end + 1) if check_fn(num)]


def _solve(input_line: str, check_fn: Callable[[int], bool]) -> int:
    ranges = parse_ranges(input_line)
    total = 0
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, check_fn)
        total += sum(invalid_ids)
    return total


def solve_part1(input_line: str) -> int:
    """Solve Part 1 using exact two-repeat rule."""
    return _solve(input_line, is_invalid_part1)


def solve_part2(input_line: str) -> int:
    """Solve Part 2 using at-least-two-repeat rule."""
    return _solve(input_line, is_invalid_part2)

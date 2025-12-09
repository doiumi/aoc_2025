"""
Shared helpers for Advent of Code solutions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

Range = Tuple[int, int]


def read_text(path: str | Path) -> str:
    """Read a file as text, stripping trailing whitespace."""
    return Path(path).read_text().strip()


def parse_ranges(line: str) -> List[Range]:
    """Parse a comma-separated list of ranges like '11-22,95-115'."""
    ranges: List[Range] = []
    if not line.strip():
        return ranges
    for range_str in line.strip().split(","):
        start, end = range_str.split("-")
        ranges.append((int(start), int(end)))
    return ranges


def has_repeated_pattern(num: int, *, min_repeats: int = 2, exact_repeats: int | None = None) -> bool:
    """
    Check whether a number is composed of a repeated digit pattern.

    Args:
        num: Number to check.
        min_repeats: Minimum number of pattern repetitions required.
        exact_repeats: If provided, require exactly this many repetitions.
    """
    s = str(num)
    length = len(s)
    if length < min_repeats:
        return False

    for pattern_len in range(1, length // min_repeats + 1):
        if length % pattern_len != 0:
            continue

        repeats = length // pattern_len
        if repeats < min_repeats:
            continue
        if exact_repeats is not None and repeats != exact_repeats:
            continue

        pattern = s[:pattern_len]
        if pattern * repeats == s:
            return True

    return False

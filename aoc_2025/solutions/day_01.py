"""
Day 1: Secret Entrance - Dial Safe Password Solver

Part 1: Count times the dial lands on 0 after a rotation completes.
Part 2: Count times the dial passes through 0 during or after any rotation.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Rotation = Tuple[str, int]

DIAL_SIZE = 100
START_POSITION = 50


def parse_rotations(text: str) -> List[Rotation]:
    """Parse rotation commands from raw text."""
    rotations: List[Rotation] = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def apply_rotation(current_position: int, direction: str, distance: int) -> int:
    """Apply a single rotation on the dial."""
    if direction == "L":
        return (current_position - distance) % DIAL_SIZE
    return (current_position + distance) % DIAL_SIZE


def count_zeros_ending(rotations: Sequence[Rotation]) -> int:
    """
    PART 1: Count times the dial lands on 0 at the end of each rotation.
    """
    current_position = START_POSITION
    zero_count = 0

    for direction, distance in rotations:
        current_position = apply_rotation(current_position, direction, distance)
        if current_position == 0:
            zero_count += 1

    return zero_count


def count_zeros_passing(rotations: Sequence[Rotation]) -> int:
    """
    PART 2: Count every time the dial reaches position 0 during or after a rotation.
    """
    current_position = START_POSITION
    zero_count = 0

    for direction, distance in rotations:
        if direction == "R":
            # Moving right crosses 0 every full dial revolution.
            zero_count += (current_position + distance) // DIAL_SIZE
            current_position = (current_position + distance) % DIAL_SIZE
        else:
            # Moving left may wrap backward past 0.
            if current_position > 0 and distance >= current_position:
                remaining = distance - current_position
                zero_count += 1 + (remaining // DIAL_SIZE)
            else:
                zero_count += distance // DIAL_SIZE
            current_position = (current_position - distance) % DIAL_SIZE

    return zero_count


def solve_part1(text: str) -> int:
    """Solve Part 1 for Day 1 using the provided input text."""
    rotations = parse_rotations(text)
    return count_zeros_ending(rotations)


def solve_part2(text: str) -> int:
    """Solve Part 2 for Day 1 using the provided input text."""
    rotations = parse_rotations(text)
    return count_zeros_passing(rotations)

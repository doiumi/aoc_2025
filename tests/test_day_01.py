import pytest

from aoc_2025.solutions.day_01 import (
    apply_rotation,
    count_zeros_ending,
    count_zeros_passing,
    parse_rotations,
    solve_part1,
    solve_part2,
)


class TestApplyRotation:
    def test_right_rotation_basic(self):
        assert apply_rotation(11, "R", 8) == 19

    def test_left_rotation_basic(self):
        assert apply_rotation(19, "L", 19) == 0

    def test_left_rotation_wrapping(self):
        assert apply_rotation(5, "L", 10) == 95

    def test_right_rotation_wrapping(self):
        assert apply_rotation(95, "R", 5) == 0

    def test_rotation_full_circle(self):
        assert apply_rotation(50, "R", 100) == 50
        assert apply_rotation(50, "L", 100) == 50

    def test_rotation_multiple_circles(self):
        assert apply_rotation(50, "R", 150) == 0
        assert apply_rotation(50, "L", 150) == 0

    def test_rotation_zero_distance(self):
        assert apply_rotation(50, "R", 0) == 50
        assert apply_rotation(50, "L", 0) == 50


class TestCountZerosEnding:
    def test_example_from_puzzle(self):
        example_rotations = [
            ("L", 68),
            ("L", 30),
            ("R", 48),
            ("L", 5),
            ("R", 60),
            ("L", 55),
            ("L", 1),
            ("L", 99),
            ("R", 14),
            ("L", 82),
        ]
        assert count_zeros_ending(example_rotations) == 3

    def test_immediate_zero(self):
        rotations = [("R", 50)]
        assert count_zeros_ending(rotations) == 1

    def test_no_zeros(self):
        rotations = [("R", 10), ("R", 10), ("R", 10)]
        assert count_zeros_ending(rotations) == 0

    def test_multiple_zeros(self):
        rotations = [("R", 50), ("R", 50), ("R", 50)]
        assert count_zeros_ending(rotations) == 2


class TestCountZerosPassing:
    def test_example_from_puzzle_part2(self):
        example_rotations = [
            ("L", 68),
            ("L", 30),
            ("R", 48),
            ("L", 5),
            ("R", 60),
            ("L", 55),
            ("L", 1),
            ("L", 99),
            ("R", 14),
            ("L", 82),
        ]
        assert count_zeros_passing(example_rotations) == 6

    def test_large_right_rotation(self):
        rotations = [("R", 1000)]
        assert count_zeros_passing(rotations) == 10

    def test_right_rotation_single_pass(self):
        rotations = [("R", 50)]
        assert count_zeros_passing(rotations) == 1

    def test_left_rotation_wrapping(self):
        rotations = [("L", 50)]
        assert count_zeros_passing(rotations) >= 1

    def test_left_rotation_no_zero(self):
        rotations = [("L", 10)]
        assert count_zeros_passing(rotations) == 0

    def test_right_rotation_no_zero(self):
        rotations = [("R", 30)]
        assert count_zeros_passing(rotations) == 0


class TestParseRotations:
    def test_parse_simple_input(self):
        rotations = parse_rotations("L68\nR30\nL15\n")
        assert rotations == [("L", 68), ("R", 30), ("L", 15)]

    def test_parse_large_distances(self):
        rotations = parse_rotations("R1000\nL9999\n")
        assert rotations == [("R", 1000), ("L", 9999)]

    def test_parse_empty_lines(self):
        rotations = parse_rotations("L10\n\nR20\n\n")
        assert rotations == [("L", 10), ("R", 20)]


class TestIntegration:
    def test_part1_and_part2_consistency(self):
        example_rotations = [
            ("L", 68),
            ("L", 30),
            ("R", 48),
            ("L", 5),
            ("R", 60),
            ("L", 55),
            ("L", 1),
            ("L", 99),
            ("R", 14),
            ("L", 82),
        ]
        part1 = count_zeros_ending(example_rotations)
        part2 = count_zeros_passing(example_rotations)
        assert part2 >= part1

    def test_solvers(self):
        input_text = "L50\nR50\n"
        assert solve_part1(input_text) == 1
        assert solve_part2(input_text) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Unit tests for Day 1: Secret Entrance - Dial Safe Password Solver

These tests verify the correctness of the rotation logic and zero-counting algorithms.
Run with: python -m pytest test_solution.py -v
"""

import pytest
from solution import (
    apply_rotation,
    count_zeros_ending,
    count_zeros_passing_optimized,
    parse_rotations
)


class TestApplyRotation:
    """Test the basic rotation logic."""
    
    def test_right_rotation_basic(self):
        """Test a simple right rotation."""
        # From the puzzle: if at 11, R8 goes to 19
        assert apply_rotation(11, 'R', 8) == 19
    
    def test_left_rotation_basic(self):
        """Test a simple left rotation."""
        # From the puzzle: at 19, L19 goes to 0
        assert apply_rotation(19, 'L', 19) == 0
    
    def test_left_rotation_wrapping(self):
        """Test left rotation with wraparound."""
        # From the puzzle: at 5, L10 goes to 95
        assert apply_rotation(5, 'L', 10) == 95
    
    def test_right_rotation_wrapping(self):
        """Test right rotation with wraparound."""
        # From the puzzle: at 95, R5 goes to 0
        assert apply_rotation(95, 'R', 5) == 0
    
    def test_rotation_full_circle(self):
        """Test that rotating 100 positions returns to same position."""
        assert apply_rotation(50, 'R', 100) == 50
        assert apply_rotation(50, 'L', 100) == 50
    
    def test_rotation_multiple_circles(self):
        """Test rotation greater than 100."""
        # R150 from 50 = 50 + 150 = 200 % 100 = 0
        assert apply_rotation(50, 'R', 150) == 0
        # L150 from 50 = (50 - 150) % 100 = -100 % 100 = 0
        assert apply_rotation(50, 'L', 150) == 0
    
    def test_rotation_zero_distance(self):
        """Test rotation with zero distance."""
        assert apply_rotation(50, 'R', 0) == 50
        assert apply_rotation(50, 'L', 0) == 50


class TestCountZerosEnding:
    """Test Part 1: counting times dial lands on 0 at rotation end."""
    
    def test_example_from_puzzle(self):
        """Test with the example from puzzle description."""
        # The example rotations: L68, L30, R48, L5, R60, L55, L1, L99, R14, L82
        # Expected to land on 0 exactly 3 times
        example_rotations = [
            ('L', 68),
            ('L', 30),
            ('R', 48),
            ('L', 5),
            ('R', 60),
            ('L', 55),
            ('L', 1),
            ('L', 99),
            ('R', 14),
            ('L', 82),
        ]
        assert count_zeros_ending(example_rotations) == 3
    
    def test_immediate_zero(self):
        """Test landing on 0 on first rotation."""
        rotations = [('R', 50)]  # Start at 50, go right 50 = 100 % 100 = 0
        assert count_zeros_ending(rotations) == 1
    
    def test_no_zeros(self):
        """Test when dial never lands on 0."""
        rotations = [
            ('R', 10),  # 50 + 10 = 60
            ('R', 10),  # 60 + 10 = 70
            ('R', 10),  # 70 + 10 = 80
        ]
        assert count_zeros_ending(rotations) == 0
    
    def test_multiple_zeros(self):
        """Test landing on 0 multiple times."""
        rotations = [
            ('R', 50),   # 50 + 50 = 100 % 100 = 0 (hit 1)
            ('R', 50),   # 0 + 50 = 50
            ('R', 50),   # 50 + 50 = 100 % 100 = 0 (hit 2)
        ]
        assert count_zeros_ending(rotations) == 2


class TestCountZerosPassing:
    """Test Part 2: counting times dial passes through 0 during/after rotation."""
    
    def test_example_from_puzzle_part2(self):
        """Test with the example from puzzle Part 2 description."""
        # Same rotations but now count intermediate passes too
        # Expected answer: 6 (3 from landing on 0 + 3 from passing during rotation)
        example_rotations = [
            ('L', 68),
            ('L', 30),
            ('R', 48),
            ('L', 5),
            ('R', 60),
            ('L', 55),
            ('L', 1),
            ('L', 99),
            ('R', 14),
            ('L', 82),
        ]
        assert count_zeros_passing_optimized(example_rotations) == 6
    
    def test_large_right_rotation(self):
        """Test right rotation that passes through 0 multiple times."""
        # From the puzzle: R1000 from 50 should pass through 0 ten times
        rotations = [('R', 1000)]
        assert count_zeros_passing_optimized(rotations) == 10
    
    def test_right_rotation_single_pass(self):
        """Test right rotation that passes through 0 exactly once."""
        # From 50, R50 = 100 (1 pass through 0)
        rotations = [('R', 50)]
        assert count_zeros_passing_optimized(rotations) == 1
    
    def test_left_rotation_wrapping(self):
        """Test left rotation that wraps and passes through 0."""
        # From 30, L50 wraps around: goes left 30 to hit 0, then 20 more
        # That's 1 pass (at 0) + 0 more = 1
        rotations = [('L', 50)]
        result = count_zeros_passing_optimized(rotations)
        assert result >= 1, f"Expected at least 1 pass through 0, got {result}"
    
    def test_left_rotation_no_zero(self):
        """Test left rotation that doesn't reach 0."""
        # From 50, L10 goes to 40, never hits 0
        rotations = [('L', 10)]
        assert count_zeros_passing_optimized(rotations) == 0
    
    def test_right_rotation_no_zero(self):
        """Test right rotation that doesn't pass through 0."""
        # From 50, R30 goes to 80, never hits 0
        rotations = [('R', 30)]
        assert count_zeros_passing_optimized(rotations) == 0


class TestParseRotations:
    """Test the input file parsing."""
    
    def test_parse_simple_input(self, tmp_path):
        """Test parsing a simple input file."""
        test_file = tmp_path / "test_input.txt"
        test_file.write_text("L68\nR30\nL15\n")
        
        rotations = parse_rotations(str(test_file))
        
        assert len(rotations) == 3
        assert rotations[0] == ('L', 68)
        assert rotations[1] == ('R', 30)
        assert rotations[2] == ('L', 15)
    
    def test_parse_large_distances(self, tmp_path):
        """Test parsing large distance values."""
        test_file = tmp_path / "test_input.txt"
        test_file.write_text("R1000\nL9999\n")
        
        rotations = parse_rotations(str(test_file))
        
        assert rotations[0] == ('R', 1000)
        assert rotations[1] == ('L', 9999)
    
    def test_parse_empty_lines(self, tmp_path):
        """Test parsing with empty lines."""
        test_file = tmp_path / "test_input.txt"
        test_file.write_text("L10\n\nR20\n\n")
        
        rotations = parse_rotations(str(test_file))
        
        assert len(rotations) == 2
        assert rotations[0] == ('L', 10)
        assert rotations[1] == ('R', 20)


class TestIntegration:
    """Integration tests for complete scenarios."""
    
    def test_part1_and_part2_consistency(self):
        """Verify Part 2 is always >= Part 1 (passes include landings)."""
        example_rotations = [
            ('L', 68), ('L', 30), ('R', 48), ('L', 5),
            ('R', 60), ('L', 55), ('L', 1), ('L', 99),
            ('R', 14), ('L', 82),
        ]
        part1 = count_zeros_ending(example_rotations)
        part2 = count_zeros_passing_optimized(example_rotations)
        
        # Part 2 must be >= Part 1 (all endings are also passings)
        assert part2 >= part1, f"Part 2 ({part2}) should be >= Part 1 ({part1})"
    
    def test_starting_position(self):
        """Verify the dial always starts at position 50."""
        # This is implicit in the tests but good to be explicit
        # A rotation of L50 from 50 should go to 0
        rotations = [('L', 50)]
        result = count_zeros_ending(rotations)
        assert result == 1, "Starting at 50 and rotating L50 should land on 0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

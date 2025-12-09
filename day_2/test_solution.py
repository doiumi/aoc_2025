"""
Unit tests for Day 2: Gift Shop solution
"""

import unittest
from solution import is_invalid_id, parse_ranges, find_invalid_ids_in_range, solve


class TestIsInvalidId(unittest.TestCase):
    """Test cases for is_invalid_id function"""
    
    def test_single_digit_repeated(self):
        """Test single digit repeated twice (e.g., 55)"""
        self.assertTrue(is_invalid_id(55))
        self.assertTrue(is_invalid_id(11))
        self.assertTrue(is_invalid_id(99))
    
    def test_two_digits_repeated(self):
        """Test two digits repeated twice (e.g., 6464)"""
        self.assertTrue(is_invalid_id(6464))
        self.assertTrue(is_invalid_id(1212))
        self.assertTrue(is_invalid_id(9090))
    
    def test_three_digits_repeated(self):
        """Test three digits repeated twice (e.g., 123123)"""
        self.assertTrue(is_invalid_id(123123))
        self.assertTrue(is_invalid_id(456456))
        self.assertTrue(is_invalid_id(999999))
    
    def test_odd_length_numbers(self):
        """Odd length numbers cannot be invalid IDs"""
        self.assertFalse(is_invalid_id(5))
        self.assertFalse(is_invalid_id(555))
        self.assertFalse(is_invalid_id(12345))
    
    def test_even_length_not_repeated(self):
        """Even length but not a repeated pattern"""
        self.assertFalse(is_invalid_id(12))
        self.assertFalse(is_invalid_id(1234))
        self.assertFalse(is_invalid_id(101010))
    
    def test_edge_cases(self):
        """Test edge cases"""
        self.assertTrue(is_invalid_id(22))
        self.assertFalse(is_invalid_id(101))  # Leading zero in second half


class TestParseRanges(unittest.TestCase):
    """Test cases for parse_ranges function"""
    
    def test_single_range(self):
        """Test parsing a single range"""
        result = parse_ranges("11-22")
        self.assertEqual(result, [(11, 22)])
    
    def test_multiple_ranges(self):
        """Test parsing multiple ranges"""
        result = parse_ranges("11-22,95-115,998-1012")
        self.assertEqual(result, [(11, 22), (95, 115), (998, 1012)])
    
    def test_large_numbers(self):
        """Test parsing ranges with large numbers"""
        result = parse_ranges("1188511880-1188511890,222220-222224")
        self.assertEqual(result, [(1188511880, 1188511890), (222220, 222224)])
    
    def test_with_whitespace(self):
        """Test parsing with leading/trailing whitespace"""
        result = parse_ranges("  11-22,95-115  ")
        self.assertEqual(result, [(11, 22), (95, 115)])


class TestFindInvalidIdsInRange(unittest.TestCase):
    """Test cases for find_invalid_ids_in_range function"""
    
    def test_simple_range_with_invalid_ids(self):
        """Test range from puzzle example: 11-22 has 11 and 22"""
        result = find_invalid_ids_in_range(11, 22)
        self.assertEqual(result, [11, 22])
    
    def test_range_with_single_invalid_id(self):
        """Test range from puzzle example: 95-115 has 99"""
        result = find_invalid_ids_in_range(95, 115)
        self.assertEqual(result, [99])
    
    def test_range_with_no_invalid_ids(self):
        """Test range from puzzle example: 1698522-1698528 has no invalid IDs"""
        result = find_invalid_ids_in_range(1698522, 1698528)
        self.assertEqual(result, [])
    
    def test_large_range(self):
        """Test a large range"""
        result = find_invalid_ids_in_range(998, 1012)
        self.assertEqual(result, [1010])
    
    def test_single_number_invalid(self):
        """Test range with single number that is invalid"""
        result = find_invalid_ids_in_range(55, 55)
        self.assertEqual(result, [55])
    
    def test_single_number_valid(self):
        """Test range with single number that is valid"""
        result = find_invalid_ids_in_range(56, 56)
        self.assertEqual(result, [])


class TestSolve(unittest.TestCase):
    """Test cases for solve function"""
    
    def test_example_input(self):
        """Test with the example from the puzzle"""
        example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        result = solve(example_input)
        # From puzzle: 11 + 22 + 99 + 1010 + 1188511885 + 222222 + 446446 + 38593859 = 1227775554
        self.assertEqual(result, 1227775554)
    
    def test_simple_input(self):
        """Test with a simple input"""
        simple_input = "11-22"
        result = solve(simple_input)
        self.assertEqual(result, 33)  # 11 + 22
    
    def test_multiple_ranges(self):
        """Test with multiple ranges"""
        input_data = "55-55,6464-6464"
        result = solve(input_data)
        self.assertEqual(result, 6519)  # 55 + 6464


if __name__ == "__main__":
    unittest.main()

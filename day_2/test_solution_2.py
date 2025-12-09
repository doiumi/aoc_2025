"""
Unit tests for Day 2: Gift Shop Part 2 solution
"""

import unittest
from solution_2 import is_invalid_id_part2, parse_ranges, find_invalid_ids_in_range, solve


class TestIsInvalidIdPart2(unittest.TestCase):
    """Test cases for is_invalid_id_part2 function"""
    
    def test_single_digit_repeated(self):
        """Test single digit repeated multiple times (e.g., 11, 111, 1111)"""
        self.assertTrue(is_invalid_id_part2(11))
        self.assertTrue(is_invalid_id_part2(111))
        self.assertTrue(is_invalid_id_part2(1111))
        self.assertTrue(is_invalid_id_part2(1111111))
        self.assertTrue(is_invalid_id_part2(99))
        self.assertTrue(is_invalid_id_part2(999))
    
    def test_two_digits_repeated(self):
        """Test two digits repeated multiple times (e.g., 1212, 121212)"""
        self.assertTrue(is_invalid_id_part2(1212))
        self.assertTrue(is_invalid_id_part2(121212))
        self.assertTrue(is_invalid_id_part2(6464))
        self.assertTrue(is_invalid_id_part2(646464))
    
    def test_three_digits_repeated(self):
        """Test three digits repeated multiple times (e.g., 123123, 123123123)"""
        self.assertTrue(is_invalid_id_part2(123123))
        self.assertTrue(is_invalid_id_part2(123123123))
        self.assertTrue(is_invalid_id_part2(456456456))
    
    def test_four_digits_repeated(self):
        """Test four digits repeated multiple times (e.g., 12341234)"""
        self.assertTrue(is_invalid_id_part2(12341234))
        self.assertTrue(is_invalid_id_part2(12345678123456781234567812345678))
    
    def test_odd_length_numbers(self):
        """Single digit cannot be invalid ID, but odd repeats like 555 are valid"""
        self.assertFalse(is_invalid_id_part2(5))
        self.assertTrue(is_invalid_id_part2(555))  # 5 repeated 3 times
        self.assertFalse(is_invalid_id_part2(12345))  # Cannot divide evenly
    
    def test_even_length_not_repeated(self):
        """Even length but not a repeated pattern"""
        self.assertFalse(is_invalid_id_part2(12))
        self.assertFalse(is_invalid_id_part2(1234))
        self.assertFalse(is_invalid_id_part2(123456))
    
    def test_edge_cases(self):
        """Test edge cases"""
        self.assertTrue(is_invalid_id_part2(22))
        self.assertFalse(is_invalid_id_part2(101))  # Not a repeated pattern
        self.assertTrue(is_invalid_id_part2(1010))  # 10 repeated 2 times
    
    def test_puzzle_examples(self):
        """Test examples from the puzzle description"""
        # From Part 2: 12341234 (1234 two times), 123123123 (123 three times),
        # 1212121212 (12 five times), and 1111111 (1 seven times)
        self.assertTrue(is_invalid_id_part2(12341234))
        self.assertTrue(is_invalid_id_part2(123123123))
        self.assertTrue(is_invalid_id_part2(1212121212))
        self.assertTrue(is_invalid_id_part2(1111111))


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


class TestFindInvalidIdsInRange(unittest.TestCase):
    """Test cases for find_invalid_ids_in_range function"""
    
    def test_simple_range_with_invalid_ids(self):
        """Test range from puzzle example: 11-22 has 11 and 22"""
        result = find_invalid_ids_in_range(11, 22)
        self.assertEqual(result, [11, 22])
    
    def test_range_with_multiple_invalid_ids(self):
        """Test range from puzzle example: 95-115 now has 99 and 111"""
        result = find_invalid_ids_in_range(95, 115)
        self.assertEqual(result, [99, 111])
    
    def test_large_range(self):
        """Test range from puzzle example: 998-1012 has 999 and 1010"""
        result = find_invalid_ids_in_range(998, 1012)
        self.assertEqual(result, [999, 1010])
    
    def test_range_with_no_invalid_ids(self):
        """Test range from puzzle example: 1698522-1698528 has no invalid IDs"""
        result = find_invalid_ids_in_range(1698522, 1698528)
        self.assertEqual(result, [])
    
    def test_single_number_invalid(self):
        """Test range with single number that is invalid"""
        result = find_invalid_ids_in_range(55, 55)
        self.assertEqual(result, [55])


class TestSolve(unittest.TestCase):
    """Test cases for solve function"""
    
    def test_example_input(self):
        """Test with the example from the puzzle Part 2"""
        example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        result = solve(example_input)
        # From puzzle Part 2: Expected sum is 4174379265
        self.assertEqual(result, 4174379265)
    
    def test_simple_input(self):
        """Test with a simple input"""
        simple_input = "11-22"
        result = solve(simple_input)
        self.assertEqual(result, 33)  # 11 + 22
    
    def test_multiple_patterns(self):
        """Test with multiple repeating patterns"""
        input_data = "55-55,111-111,1212-1212"
        result = solve(input_data)
        self.assertEqual(result, 1378)  # 55 + 111 + 1212


if __name__ == "__main__":
    unittest.main()

"""
Day 2: Gift Shop - Invalid Product ID Finder

Problem: Find all invalid product IDs in given ranges.
Invalid IDs are numbers made only of a sequence of digits repeated twice.
Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
"""


def is_invalid_id(num: int) -> bool:
    """
    Check if a number is an invalid ID.
    
    An invalid ID is a number made of some sequence of digits repeated twice.
    For example: 55 (5 twice), 6464 (64 twice), 123123 (123 twice).
    
    Args:
        num: The number to check
        
    Returns:
        True if the number is an invalid ID, False otherwise
    """
    s = str(num)
    length = len(s)
    
    # Invalid ID must have even length
    if length % 2 != 0:
        return False
    
    # Split in half and check if both parts are equal
    half = length // 2
    return s[:half] == s[half:]


def parse_ranges(input_line: str) -> list[tuple[int, int]]:
    """
    Parse a comma-separated string of ranges into a list of tuples.
    
    Each range is formatted as "start-end" (e.g., "11-22").
    
    Args:
        input_line: A string containing comma-separated ranges
        
    Returns:
        A list of tuples, each containing (start, end) of a range
    """
    ranges = []
    for range_str in input_line.strip().split(','):
        start, end = range_str.split('-')
        ranges.append((int(start), int(end)))
    return ranges


def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """
    Find all invalid IDs within a range (inclusive).
    
    Args:
        start: The start of the range (inclusive)
        end: The end of the range (inclusive)
        
    Returns:
        A list of all invalid IDs found in the range
    """
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    return invalid_ids


def solve(input_line: str) -> int:
    """
    Find all invalid IDs in all ranges and return their sum.
    
    Args:
        input_line: A string containing comma-separated ranges
        
    Returns:
        The sum of all invalid IDs found
    """
    ranges = parse_ranges(input_line)
    total = 0
    
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)
    
    return total


if __name__ == "__main__":
    # Read input and solve
    with open("input.txt", "r") as f:
        input_data = f.read()
    
    result = solve(input_data)
    print(str(result))

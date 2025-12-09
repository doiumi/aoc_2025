"""
Day 2: Gift Shop - Part 2 - Invalid Product ID Finder (Revised Rules)

Problem: Find all invalid product IDs in given ranges using revised rules.
Invalid IDs are numbers made of some sequence of digits repeated at least twice.
Examples: 12341234 (1234 twice), 123123123 (123 three times), 1111111 (1 seven times)
"""


def is_invalid_id_part2(num: int) -> bool:
    """
    Check if a number is an invalid ID under Part 2 rules.
    
    An invalid ID is a number made of some sequence of digits repeated at least twice.
    For example: 12341234 (1234 twice), 123123123 (123 three times), 1111111 (1 seven times).
    
    Args:
        num: The number to check
        
    Returns:
        True if the number is an invalid ID, False otherwise
    """
    s = str(num)
    length = len(s)
    
    # Try each possible pattern length (from 1 to length//2)
    for pattern_len in range(1, length // 2 + 1):
        # Only valid if total length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if the entire string is made of this pattern repeated
            num_repeats = length // pattern_len
            if pattern * num_repeats == s:
                return True
    
    return False


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
    Find all invalid IDs within a range (inclusive) using Part 2 rules.
    
    Args:
        start: The start of the range (inclusive)
        end: The end of the range (inclusive)
        
    Returns:
        A list of all invalid IDs found in the range
    """
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id_part2(num):
            invalid_ids.append(num)
    return invalid_ids


def solve(input_line: str) -> int:
    """
    Find all invalid IDs in all ranges and return their sum using Part 2 rules.
    
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

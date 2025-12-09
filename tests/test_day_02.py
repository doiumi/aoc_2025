import pytest

from aoc_2025.solutions.day_02 import (
    find_invalid_ids_in_range,
    is_invalid_part1,
    is_invalid_part2,
    solve_part1,
    solve_part2,
)
from aoc_2025.utils import parse_ranges


def test_is_invalid_part1_examples():
    assert is_invalid_part1(55)
    assert is_invalid_part1(6464)
    assert is_invalid_part1(123123)
    assert not is_invalid_part1(5)
    assert not is_invalid_part1(12345)
    assert not is_invalid_part1(101010)


def test_is_invalid_part2_examples():
    assert is_invalid_part2(11)
    assert is_invalid_part2(1111)
    assert is_invalid_part2(1212)
    assert is_invalid_part2(123123123)
    assert is_invalid_part2(1111111)
    assert not is_invalid_part2(5)
    assert not is_invalid_part2(1234)


def test_parse_ranges():
    result = parse_ranges("11-22,95-115,998-1012")
    assert result == [(11, 22), (95, 115), (998, 1012)]


def test_find_invalid_ids_part1():
    assert find_invalid_ids_in_range(11, 22, is_invalid_part1) == [11, 22]
    assert find_invalid_ids_in_range(95, 115, is_invalid_part1) == [99]


def test_find_invalid_ids_part2():
    assert find_invalid_ids_in_range(95, 115, is_invalid_part2) == [99, 111]
    assert find_invalid_ids_in_range(998, 1012, is_invalid_part2) == [999, 1010]


def test_solve_part1_example():
    example_input = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )
    assert solve_part1(example_input) == 1227775554


def test_solve_part2_example():
    example_input = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )
    assert solve_part2(example_input) == 4174379265


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

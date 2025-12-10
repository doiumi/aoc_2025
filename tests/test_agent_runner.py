import pytest

from agent.config import ConfigError
from agent.runner import run_solver


def test_run_solver_part1_day1():
    result = run_solver(1, 1)
    assert isinstance(result, int)
    # Known answer from earlier run
    assert result == 1100


def test_run_solver_part2_day1():
    part1, part2 = run_solver(1, 2)
    assert part1 == 1100
    assert part2 == 6358


def test_missing_solver():
    with pytest.raises(ConfigError):
        run_solver(30, 1)

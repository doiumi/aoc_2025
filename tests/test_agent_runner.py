import pytest

from agent.config import ConfigError
from agent.runner import run_solver, write_outputs
from pathlib import Path


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


def test_write_outputs(tmp_path: Path):
    p1, p2 = write_outputs(5, 123, 456, base_dir=tmp_path)
    assert p1.read_text() == "123"
    assert p2.read_text() == "456"

# Advent of Code 2025

Python solutions with a single package and CLI runner.

## Layout
- `aoc_2025/solutions/day_01.py`, `day_02.py`: solvers with `solve_part1/solve_part2`.
- `aoc_2025/utils.py`: shared helpers (range parsing, repeated-pattern checks).
- `inputs/day_XX.txt`: puzzle inputs (copied from the site).
- `puzzles/day_XX_partY.txt`: puzzle statements.
- `tests/`: pytest suites aligned to days.

## Setup
```
python -m venv .venv
.venv\Scripts\activate  # on Windows
pip install -r requirements.txt  # add dependencies here as needed
```

## Run a solution
```
python -m aoc_2025 --day 2 --part 1 --input inputs/day_02.txt
```
`--input` is optional; by default it uses `inputs/day_XX.txt`.

Quick examples using the bundled inputs:
```
python -m aoc_2025 --day 1 --part 1    # => 1100
python -m aoc_2025 --day 1 --part 2    # => 6358
python -m aoc_2025 --day 2 --part 1    # => 31210613313
python -m aoc_2025 --day 2 --part 2    # => 41823587546
```

## Tests
```
pytest
```

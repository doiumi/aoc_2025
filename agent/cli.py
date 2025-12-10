"""
Command-line interface for the AoC agent.
"""

from __future__ import annotations

import argparse
import sys

from agent.config import ConfigError, load_config, validate_day, validate_part
from agent.errors import FetchError, LockedDayError
from agent.fetch import fetch_input, fetch_puzzle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AoC 2025 automation agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch
    fetch_parser = subparsers.add_parser("fetch", help="Fetch puzzle and input for a day")
    fetch_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")

    # solve
    solve_parser = subparsers.add_parser("solve", help="Run solver for a day/part")
    solve_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")
    solve_parser.add_argument("--part", type=int, choices=[1, 2], required=True, help="Puzzle part (1 or 2)")
    solve_parser.add_argument("--input", type=str, default=None, help="Path to input file (defaults to inputs/day_XX.txt)")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate solver output (samples/tests)")
    validate_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")
    validate_parser.add_argument("--part", type=int, choices=[1, 2], required=True, help="Puzzle part (1 or 2)")

    # submit
    submit_parser = subparsers.add_parser("submit", help="Submit an answer safely")
    submit_parser.add_argument("--day", type=int, required=True, help="Day number (1-25)")
    submit_parser.add_argument("--part", type=int, choices=[1, 2], required=True, help="Puzzle part (1 or 2)")
    submit_parser.add_argument("--answer", type=str, default=None, help="Answer to submit (default: compute via solver)")
    submit_parser.add_argument("--confirm", action="store_true", help="Required flag to actually submit")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config()
        day = validate_day(args.day)
        part = validate_part(getattr(args, "part", 1)) if hasattr(args, "part") else None
    except ConfigError as exc:
        parser.error(str(exc))
        return 2

    match args.command:
        case "fetch":
            try:
                puzzle = fetch_puzzle(day, config)
                puzzle_msg = f"puzzle ({puzzle.source}) -> {puzzle.path}"
            except LockedDayError as exc:
                parser.error(str(exc))
                return 2
            except FetchError as exc:
                parser.error(f"Failed to fetch puzzle: {exc}")
                return 2

            try:
                input_res = fetch_input(day, config)
                input_msg = f"input ({input_res.source}) -> {input_res.path}"
            except FetchError as exc:
                parser.error(f"Failed to fetch input: {exc}")
                return 2

            print(f"[agent] Fetched {puzzle_msg}")
            print(f"[agent] Fetched {input_msg}")
            return 0
        case "solve":
            print(f"[agent] Solve stub: day {day} part {part} input={args.input or 'default'}")
            return 0
        case "validate":
            print(f"[agent] Validate stub: day {day} part {part}")
            return 0
        case "submit":
            if not args.confirm:
                print("[agent] Submission requires --confirm flag. Aborting.")
                return 1
            print(f"[agent] Submit stub: day {day} part {part} answer={args.answer or '<computed>'}")
            return 0
        case _:
            parser.error("Unknown command")
            return 2


if __name__ == "__main__":
    sys.exit(main())

"""
Agent-specific exceptions.
"""


class FetchError(Exception):
    """Raised when fetching puzzle or input fails."""


class LockedDayError(FetchError):
    """Raised when a requested day is not yet available."""

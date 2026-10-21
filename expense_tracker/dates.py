"""Date handling.

Dates are stored and compared as ISO 8601 ``YYYY-MM-DD`` strings (see
``models.Expense.date``). Parsing normalises whatever the user typed into
that canonical, zero-padded form, which is what makes plain string
comparison between two dates also a correct chronological comparison.
"""

from __future__ import annotations

from datetime import date


class DateError(ValueError):
    """Raised when a date string cannot be parsed as an ISO 8601 date."""


def parse_date(raw: str) -> str:
    """Parse a user-supplied date into a canonical ``YYYY-MM-DD`` string.

    Args:
        raw: The date as typed by the user, e.g. ``"2026-01-15"``.

    Returns:
        The same date normalised to ``YYYY-MM-DD``. Normalising matters
        because Python 3.11+ also accepts forms like ``"20260115"``, which
        would compare incorrectly against the stored hyphenated dates.

    Raises:
        DateError: If the value is blank or not a valid ISO 8601 date.
    """
    text = (raw or "").strip()
    try:
        return date.fromisoformat(text).isoformat()
    except ValueError as exc:
        raise DateError("Date is not valid") from exc

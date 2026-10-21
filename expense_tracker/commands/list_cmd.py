"""The ``list`` command: show recorded expenses."""

from __future__ import annotations

from ..dates import DateError, parse_date
from ..money import format_amount

NAME = "list"
HELP = "List expenses, optionally filtered by category and date range"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--category",
        default=None,
        help="Only show expenses in this category",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Only show expenses on or after this date, in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="Only show expenses on or before this date, in YYYY-MM-DD format",
    )


def handle(args, store) -> int:
    """Print the recorded expenses, applying any category or date filters.

    Args:
        args: Parsed CLI arguments (``category``, ``since``, ``until``).
        store: The expense store to read from.

    Returns:
        ``0`` on success, ``1`` if a supplied date could not be parsed.
    """
    try:
        since = parse_date(args.since) if args.since is not None else None
        until = parse_date(args.until) if args.until is not None else None
    except DateError as exc:
        print(f"error: {exc}")
        return 1

    expenses = store.load()
    if args.category is not None:
        expenses = [e for e in expenses if e.category == args.category]
    # Both bounds are inclusive. Dates are canonical YYYY-MM-DD, so
    # string ordering is chronological ordering.
    if since is not None:
        expenses = [e for e in expenses if e.date >= since]
    if until is not None:
        expenses = [e for e in expenses if e.date <= until]

    if not expenses:
        print("No expenses found.")
        return 0

    for e in expenses:
        note = f"  ({e.note})" if e.note else ""
        print(f"#{e.id}  {e.date}  {format_amount(e.amount_cents):>10}  {e.category}{note}")
    return 0

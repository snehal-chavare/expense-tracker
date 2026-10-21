import pytest

from expense_tracker.dates import DateError, parse_date


def test_parse_iso_date():
    assert parse_date("2026-01-15") == "2026-01-15"


def test_parse_strips_whitespace():
    assert parse_date("  2026-01-15  ") == "2026-01-15"


def test_parse_normalises_to_hyphenated_form():
    # Python 3.11+ also accepts the compact "20260115"; 3.10 rejects it.
    # Either is fine, but a parsed date must never escape in a form that
    # would sort incorrectly against the stored hyphenated dates.
    try:
        parsed = parse_date("20260115")
    except DateError:
        return
    assert parsed == "2026-01-15"


def test_parse_rejects_blank():
    with pytest.raises(DateError):
        parse_date("")


def test_parse_rejects_wrong_order():
    with pytest.raises(DateError):
        parse_date("15-01-2026")


def test_parse_rejects_impossible_day():
    with pytest.raises(DateError):
        parse_date("2026-02-30")


def test_parse_message_is_user_facing():
    with pytest.raises(DateError, match="Date is not valid"):
        parse_date("nope")

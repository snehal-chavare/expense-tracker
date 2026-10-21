from expense_tracker.commands import add, list_cmd
from tests.conftest import args, make_store


def _seed(store):
    add.handle(args(amount="10.00", category="food", date="2026-01-01", note=""), store)
    add.handle(args(amount="20.00", category="travel", date="2026-01-02", note=""), store)
    add.handle(args(amount="5.00", category="food", date="2026-01-03", note=""), store)


def test_list_all(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(args(category=None, since=None, until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 3


def test_list_filtered_by_category(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    list_cmd.handle(args(category="food", since=None, until=None), store)
    out = capsys.readouterr().out
    assert "food" in out
    assert "travel" not in out


def test_list_empty(tmp_path, capsys):
    store = make_store(tmp_path)
    code = list_cmd.handle(args(category=None, since=None, until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert "No expenses found." in out


def test_list_between_since_and_until(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(
        args(category=None, since="2026-01-02", until="2026-01-03"), store
    )
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 2
    assert "2026-01-01" not in out
    assert "2026-01-02" in out  # lower bound is inclusive
    assert "2026-01-03" in out  # upper bound is inclusive


def test_list_since_only(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(args(category=None, since="2026-01-02", until=None), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 2
    assert "2026-01-01" not in out
    assert "2026-01-02" in out  # the bound itself is included


def test_list_until_only(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(args(category=None, since=None, until="2026-01-02"), store)
    out = capsys.readouterr().out
    assert code == 0
    assert out.count("\n") == 2
    assert "2026-01-03" not in out
    assert "2026-01-02" in out  # the bound itself is included


def test_list_rejects_bad_date(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding
    code = list_cmd.handle(args(category=None, since="15-01-2026", until=None), store)
    out = capsys.readouterr().out
    assert code == 1
    assert "Date is not valid" in out

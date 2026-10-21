# Expense Tracker

A small command-line expense tracker. It records expenses to a local JSON
file and can list and delete them. It is deliberately simple: no database, no
network, no framework — just a clean, well-tested Python CLI.

## Requirements

- Python 3.10 or newer

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Usage

Run via the module:

```bash
python -m expense_tracker <command> [options]
```

### Commands

| Command | What it does |
| :------ | :----------- |
| `add AMOUNT CATEGORY DATE [--note NOTE]` | Record an expense. `DATE` is `YYYY-MM-DD`. |
| `list [--category CATEGORY] [--since YYYY-MM-DD] [--until YYYY-MM-DD]` | List expenses, optionally filtered by category and date range. Both bounds are inclusive and each works on its own. |
| `summary [--month YYYY-MM]` | Show total spending per category, optionally filtered to one month. |
| `delete ID` | Delete an expense by its id. |

### Examples

```bash
python -m expense_tracker add 12.50 groceries 2026-01-15 --note "weekly shop"
python -m expense_tracker list
python -m expense_tracker list --category groceries
python -m expense_tracker list --since 2026-01-01 --until 2026-01-31
python -m expense_tracker summary
python -m expense_tracker summary --month 2026-01
python -m expense_tracker delete 1
```

By default, data is stored in `expenses.json` in the current directory. Set
`EXPENSE_TRACKER_DATA` to use a different file.

## Development

```bash
pytest                 # run the test suite
ruff check .           # lint
ruff format .          # format
```

## Project layout

```
expense_tracker/
  cli.py               # argument parsing and dispatch
  storage.py           # JSON load/save
  models.py            # the Expense record
  money.py             # money parsing/formatting (integer cents)
  dates.py             # ISO 8601 date parsing/validation
  commands/            # one module per command
    add.py
    list_cmd.py
    summary.py
    delete.py
tests/                 # pytest suite
```

### Adding a command

Each command module exposes `add_parser(subparsers)` and
`handle(args, store)`, and is listed in `expense_tracker/commands/__init__.py`.
Copy the shape of an existing command such as `add.py`.

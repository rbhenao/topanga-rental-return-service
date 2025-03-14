# topanga_queries

## Installation

This library has no external library dependencies as it is fully written using the Python standard library.

```bash
# cd to where this README / setup.py is located
pip install -e .
```

## Usage

This project requires **Python 3.10+**.

To use the pre-loaded `challenge.db` SQLite binary, place the binary in the working directory of your service.

You can reset the DB to it's initial state by running:

```bash
python scripts/reset_db.py

# or if topanga_queries installed:
reset-db
```

Make sure that the SQLite `challenge.db` binary is at the same level as your working directory.

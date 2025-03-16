"""Main module to process a rental return event from a JSON file."""
import json
from pathlib import Path
import sys
import os
import sqlite3

from rental_return_events.logger import configure_logging
from rental_return_events.processor import process_rental_return

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PACKAGE_ROOT / "challenge.db"


def check_database():
    """Ensure the database exists and contains the required tables."""
    if not DB_PATH.exists():
        print(f"Error! challege.db not found at: {DB_PATH}")
        print("Initialize with: python -m topanga_queries.bootstrap.db")
        sys.exit(1)

    # Check for the required tables: users, assets, rentals
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}

        required_tables = {"users", "assets", "rentals"}

        if not required_tables.issubset(tables):
            print(
                f"Error: Database at {DB_PATH} is missing required tables: {
                    required_tables - tables}")
            print("Initialize with: python -m topanga_queries.bootstrap.db")
            sys.exit(1)


def load_json_file(file_path):
    """Loads the JSON file and return its contents as dictionary."""

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in {file_path}: {str(e)}")
        sys.exit(1)

    except OSError as e:
        print(f"OS error while reading {file_path}: {str(e)}")
        sys.exit(1)


def main():
    """Main function to process a rental return event from a JSON file."""

    check_database()  # Ensure the database exists and is valid

    if len(sys.argv) < 2:
        print("Usage: python main.py <event_file.json> [--verbose]")
        sys.exit(1)

    # Check for optional --verbose flag
    verbose_mode = "--verbose" in sys.argv

    # Configure logging based on verbose mode
    configure_logging(verbose=verbose_mode)

    json_file = sys.argv[1]  # read the json return event file

    try:
        payload = load_json_file(json_file)
        response = process_rental_return(payload)
        print(json.dumps(response, indent=4))  # Print structured JSON response

    except FileNotFoundError:
        print(f"Error: File not found - {json_file}")
        sys.exit(1)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file} - {str(e)}")
        sys.exit(1)

    except KeyError as e:
        print(f"Error: Missing required key in event data - {str(e)}")
        sys.exit(1)

    except ValueError as e:
        print(f"Error: Invalid return event data - {str(e)}")
        sys.exit(1)

    except OSError as e:
        print(f"Error: OS error while accessing {json_file} - {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

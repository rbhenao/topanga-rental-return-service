import pytest
import os
import sys
import shutil
import json
import sqlite3

from topanga_queries.rentals import Rental
from topanga_queries import reset_db_connection
from topanga_queries.bootstrap.db import initialize_challenge_db

# Get the absolute path to the project root (one level up from `tests/`)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define common paths
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
DB_TEST_PATH = os.path.join(os.path.dirname(__file__), "challenge.db")  # Inside `tests/`
EVENTS_DIR = os.path.join(SRC_PATH, "example_events")

# Add `src/` to sys.path for all tests.
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
    print(f"Added {SRC_PATH} to sys.path")

# Initialize the test database
initialize_challenge_db()

@pytest.fixture(scope="function", autouse=True)
def refresh_test_db():
    """Creates a clean database and resets db_connection before each test.
    """
    if os.path.exists(DB_TEST_PATH):
        os.remove(DB_TEST_PATH)

    db_connection = reset_db_connection()
    initialize_challenge_db()
    
    yield db_connection

    db_connection.close()

@pytest.fixture
def load_event():
    """Loads an event from the `example_events/` directory."""
    
    def _load_event(filename):
        event_path = os.path.join(EVENTS_DIR, filename)
        if not os.path.exists(event_path):
            pytest.fail(f"Event file not found: {event_path}")
        
        with open(event_path, "r") as f:
            return json.load(f)

    return _load_event
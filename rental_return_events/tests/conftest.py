from env_setup import PROJECT_ROOT, DB_TEST_PATH, EVENTS_DIR

import pytest
import os
import sys
import json
from pathlib import Path

# Add package to sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define paths and set up environment before importing topanga and rental_return_events packages
DB_TEST_PATH = os.path.join(os.path.dirname(__file__), "challenge.test.db")  # Inside `tests/`
os.environ["TOPANGA_DB_PATH"] = DB_TEST_PATH

from rental_return_events.logger import configure_logging
from topanga_queries.rentals import Rental
from topanga_queries import reset_db_connection
from topanga_queries.bootstrap.db import initialize_challenge_db

# Suppress debug logging during tests
configure_logging(verbose=False)

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

import os
import sys
from pathlib import Path

# Define paths and set up environment before importing packages
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Ensure the project root is in sys.path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Define database path for testing
DB_TEST_PATH = os.path.join(PROJECT_ROOT, "tests", "challenge.test.db")
os.environ["TOPANGA_DB_PATH"] = DB_TEST_PATH

# Define events directory path
EVENTS_DIR = os.path.join(PROJECT_ROOT, "topanga_queries", "example_events")
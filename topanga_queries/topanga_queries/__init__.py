import os
import sqlite3
import sys

#print("Connecting to/creating challenge.db at:", os.getcwd())

DB_NAME = os.getenv("TOPANGA_DB_PATH", "challenge.db")
db_connection = None

def initialize_db_connection():
    """Initialize `db_connection` if not already connected."""
    global db_connection

    # Determine which database to use (default to "challenge.db", override in tests)
    if db_connection is None:
        DB_NAME = "challenge.db"
        db_connection = sqlite3.connect(DB_NAME)
        db_connection.execute("PRAGMA journal_mode=WAL;")
        db_connection.commit()

initialize_db_connection()

# ====================================================
# Used For Testing
# Resets db_connection for every topanga_queries submodule
# This way we avoid needing to make source code changes to topanga_queries
# ====================================================
def reset_db_connection():
    """Closes and reopens the database connection to ensure it points to the latest DB."""
    global db_connection

    if db_connection:
        db_connection.close()  # Close old db connection

    # Reload the db environment variable and reconnect
    new_db_name = os.getenv("TOPANGA_DB_PATH", "challenge.test.db")
    db_connection = sqlite3.connect(new_db_name)
    db_connection.execute("PRAGMA journal_mode=WAL;")
    db_connection.commit()

    # Update the db_connection in the topanga_queries module
    sys.modules["topanga_queries"].db_connection = db_connection

    # Update the db_connection in all topanga_queries submodules
    for module in sys.modules:
        if module.startswith("topanga_queries.") and hasattr(sys.modules[module], "db_connection"):
            setattr(sys.modules[module], "db_connection", db_connection)
    
    return db_connection
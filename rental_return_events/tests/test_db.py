import sqlite3

def test_db_connection(refresh_test_db):
    """Test if the database connection can be established."""

    try:
        cur = refresh_test_db.cursor()
        cur.execute("SELECT 1")  # Simple query to check connection
        cur.close()
        assert True  # Test passes if no exceptions raised
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_tables_exist(refresh_test_db):
    """Test if all three required tables exist in the database."""

    cur = refresh_test_db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cur.fetchall()}  # Convert to set for easy comparison
    cur.close()

    expected_tables = {"users", "assets", "rentals"}
    assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"

def test_table_schema(refresh_test_db):
    """Test if tables have the correct schema."""

    cur = refresh_test_db.cursor()
    
    table_schemas = {
        "users": {"id", "name"},
        "assets": {"id", "asset_type"},
        "rentals": {
            "id", "user_id", "asset_id", "created_at_location_id", "created_at",
            "expires_at", "status", "eligible_asset_types", "returned_at_location_id", "returned_at"
        },
    }

    for table, expected_columns in table_schemas.items():
        cur.execute(f"PRAGMA table_info({table});")
        actual_columns = {row[1] for row in cur.fetchall()}
        #print(f"Checking `{table}` schema. Expected: {expected_columns}, Found: {actual_columns}")
        assert expected_columns == actual_columns, f"Table `{table}` schema mismatch!"
    
    cur.close()
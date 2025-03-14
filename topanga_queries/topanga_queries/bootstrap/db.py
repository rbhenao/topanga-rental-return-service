import json
import uuid
from datetime import datetime, timedelta, timezone

from topanga_queries import db_connection

def init_tables(cur) -> None:
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id TEXT NOT NULL PRIMARY KEY,
                    name TEXT
                );
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS assets(
                    id TEXT NOT NULL PRIMARY KEY,
                    asset_type TEXT NOT NULL
                );
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS rentals(
                    id TEXT NOT NULL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    asset_id TEXT NOT NULL,
                    created_at_location_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    eligible_asset_types JSON DEFAULT('[]'),
                    returned_at_location_id TEXT,
                    returned_at TEXT
                );
                """)
    print("Tables created in DB")


def _init_records(cur, table_name: str, data: list) -> None:
    cur.execute(f"DELETE FROM {table_name};")  # Clear all existing records
    col_placeholders = ",".join(["?" for _ in range(len(data[0]))])
    cur.executemany(
        f"INSERT INTO {table_name} VALUES({col_placeholders})",
        data,
    )
    db_connection.commit()
    print(f"{table_name} records added")


def init_users(cur) -> list:
    users = [
        ("tpg_u0001", "Adam B."),
        ("tpg_u0002", "Page S."),
        ("tpg_u0003", "Max O."),
        ("tpg_u0004", "Wesley J."),
        ("tpg_u0005", "Don B."),
    ]
    _init_records(cur, "users", users)
    # Return all user IDs
    return users


def init_assets(cur) -> list:
    ASSET_TYPES = ["3-compartment", "clamshell", "large-bowl", "small-bowl", "mug"]
    assets = [(f"tpg_a{n:05}", ASSET_TYPES[n % 5]) for n in range(1, 51)]
    _init_records(cur, "assets", assets)
    # Return all asset IDs
    return assets


# Fixed reference timestamp for consistency
REFERENCE_NOW = datetime(2025, 2, 10, 12, 0, 0, tzinfo=timezone.utc)


def generate_rental_record(
    id: str,
    user_id: str,
    asset_id: str,
    created_at_location_id: str,
    created_at: datetime,
    expires_in_days: int,
    status: str,
    returned_at_location_id: str = None,
    returned_at: datetime = None,
) -> tuple:
    eligible_map = {
        "3-compartment": ["3-compartment", "clamshell"],
        "clamshell": ["3-compartment", "clamshell"],
        "large-bowl": ["large-bowl", "small-bowl"],
        "small-bowl": ["large-bowl", "small-bowl"],
        "mug": ["mug"],
    }

    expires_at = created_at + timedelta(days=expires_in_days)
    asset_type = asset_id.split("a")[1]  # Extracting type index from ID
    asset_type = ["3-compartment", "clamshell", "large-bowl", "small-bowl", "mug"][
        int(asset_type) % 5
    ]
    eligible_asset_types = json.dumps(eligible_map[asset_type])

    return (
        id,
        user_id,
        asset_id,
        created_at_location_id,
        created_at.isoformat(),
        expires_at.isoformat(),
        status,
        eligible_asset_types,
        returned_at_location_id,
        returned_at.isoformat() if returned_at else None,
    )


def init_rentals(cur):
    rentals = [
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0001",
            "tpg_a00001",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=5),
            10,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0001",
            "tpg_a00002",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=3),
            7,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0002",
            "tpg_a00010",
            "topanga-location-02",
            REFERENCE_NOW - timedelta(days=8),
            15,
            "COMPLETED",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=1),
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0002",
            "tpg_a00015",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=1),
            5,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0003",
            "tpg_a00020",
            "topanga-location-03",
            REFERENCE_NOW - timedelta(days=2),
            6,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0004",
            "tpg_a00025",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=6),
            10,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0004",
            "tpg_a00030",
            "topanga-location-02",
            REFERENCE_NOW - timedelta(days=4),
            8,
            "COMPLETED",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=2),
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0005",
            "tpg_a00035",
            "topanga-location-03",
            REFERENCE_NOW - timedelta(days=7),
            10,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0005",
            "tpg_a00040",
            "topanga-location-01",
            REFERENCE_NOW - timedelta(days=3),
            7,
            "IN_PROGRESS",
        ),
        generate_rental_record(
            str(uuid.uuid4()),
            "tpg_u0005",
            "tpg_a00045",
            "topanga-location-02",
            REFERENCE_NOW - timedelta(days=9),
            12,
            "COMPLETED",
            "topanga-location-03",
            REFERENCE_NOW - timedelta(days=3),
        ),
    ]

    _init_records(cur, "rentals", rentals)


def initialize_challenge_db():
    cur = db_connection.cursor()
    init_tables(cur)

    init_users(cur)
    init_assets(cur)
    init_rentals(cur)

    cur.close()


if __name__ == "__main__":
    initialize_challenge_db()

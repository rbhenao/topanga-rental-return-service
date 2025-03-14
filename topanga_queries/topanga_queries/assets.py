from dataclasses import dataclass

from topanga_queries import db_connection


@dataclass
class Asset:
    id: str
    asset_type: str


def get_asset(id: str) -> Asset:
    """Get Asset from database.

    Args:
        id (str): Asset `id`

    Raises:
        ValueError: If matching asset does not exist

    Returns:
        Asset: Asset dataclass instance
    """
    cur = db_connection.cursor()
    cur.execute("""SELECT * FROM assets WHERE id = ?""", (id,))
    record = cur.fetchone()
    if record:
        return Asset(*record)
    else:
        raise ValueError("Asset not found.")

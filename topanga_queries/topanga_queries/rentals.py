from dataclasses import dataclass
from typing import List

from topanga_queries import db_connection


@dataclass
class Rental:
    id: str
    user_id: str
    asset_id: str
    created_at_location_id: str
    created_at: str
    expires_at: str
    status: str
    eligible_asset_types: list
    returned_at_location_id: str
    returned_at: str

    def __post_init__(self):
        # SQLite only stores primitive types;
        # convert JSON array string to Python list
        self.eligible_asset_types = list(eval(self.eligible_asset_types))


def get_rental(id: str) -> Rental:
    """Get Rental from database.

    Args:
        id (str): Rental `id`

    Raises:
        ValueError: Matching rental does not exist

    Returns:
        Rental: Rental dataclss instance
    """
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM rentals WHERE id = ?", (id,))
    record = cur.fetchone()
    if record:
        return Rental(*record)
    else:
        raise ValueError("Rental not found.")


def list_rentals_for_user(user_id: str) -> List[Rental]:
    """List all Rentals for a user.

    Feel free to extend or modify this helper as you see fit.
    Changing this is not necessary for completing this challenge.
    But if you do, please include a note about the change(s) in your deliverable.

    Args:
        user_id (str): User `id` to list Rentals for

    Returns:
        List[Rental]: Array of Rental dataclass instances
    """
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM rentals where user_id = ?", (user_id,))
    records = cur.fetchall()
    return [Rental(*record) for record in records]


def complete_rental(
    id: str, status: str, returned_at: str, returned_at_location_id: str
) -> None:
    """Complete Rental with provided args.

    Args:
        id (str): Rental `id` to update
        status (str): {'FORGIVEN', 'FLAGGED', 'COMPLETED'}
        returned_at (str): ISO8601 timestamp of return
        returned_at_location_id (str): Location ID of return
    """
    cur = db_connection.cursor()
    cur.execute(
        """
                UPDATE rentals
                SET status = ?,
                    returned_at = ?,
                    returned_at_location_id = ?
                WHERE id = ?
                """,
        (status, returned_at, returned_at_location_id, id),
    )
    db_connection.commit()
    cur.close()
    return get_rental(id)

from dataclasses import dataclass

from topanga_queries import db_connection


@dataclass
class User:
    id: str
    name: str


def get_user(id: str) -> User:
    """Get User from database.

    Args:
        id (str): User `id`

    Raises:
        ValueError: If matching user does not exist

    Returns:
        User: User dataclass instance
    """
    cur = db_connection.cursor()
    cur.execute("""SELECT * FROM users WHERE id = ?""", (id,))
    record = cur.fetchone()
    if record:
        return User(*record)
    else:
        raise ValueError("User not found.")

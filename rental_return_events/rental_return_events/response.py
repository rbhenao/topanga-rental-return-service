"""Response module for rental return events"""
from typing import Optional
from dataclasses import dataclass, asdict

from topanga_queries.rentals import Rental


@dataclass
class RentalReturnResponse:
    """Response object for rental return"""
    status: str  # "SUCCESS" or "FAILED"
    message: str
    rental_id: Optional[str] = None
    rental_returned_at: Optional[str] = None
    rental_status: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self):
        """Converts the response object to a dictionary for JSON serialization"""
        return asdict(self)


def create_success_response(rental: Rental) -> dict:
    """Creates a success response after rental completion.

    Args:
        rental (Rental): The rental object

    Returns:
        dict: The success response dictionary
    """
    return RentalReturnResponse(
        status="SUCCESS",
        message="Rental successfully completed",
        rental_id=rental.id,
        rental_returned_at=rental.returned_at,
        rental_status=rental.status
    ).to_dict()


def create_failure_response(message: str) -> dict:
    """Creates a failure response dictionary

    Args:
        message (str): The error message

    Returns:
        dict: The failure response dictionary
    """
    return RentalReturnResponse(
        status="FAILED",
        message=message,
        error="No eligible rental found"
    ).to_dict()

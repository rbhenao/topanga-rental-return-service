
from typing import Optional
from dataclasses import dataclass, asdict

from topanga_queries.rentals import Rental

from .return_event_utils import print_rental

@dataclass
class RentalReturnResponse:
    status: str  # "SUCCESS" or "FAILED"
    message: str
    rental_id: Optional[str] = None
    rental_returned_at: Optional[str] = None
    rental_status: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self):
        """Converts the response object to a dictionary for JSON serialization"""
        return asdict(self)

def create_success_response(rental: Rental, verbose_mode: bool) -> dict:
    """Creates a success response after rental completion.
    Args:
        rental (Rental): The rental object
        verbose_mode (bool): Flag to enable verbose logging 
    
    Returns:
        dict: The success response dictionary
    """
    print_rental(verbose_mode, rental, "UPDATED RENTAL:")
    
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
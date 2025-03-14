import json
from typing import List, Optional
from datetime import datetime

from topanga_queries.rentals import Rental, complete_rental, get_rental, list_rentals_for_user
from topanga_queries.assets import Asset, get_asset

from rental_return_events.handler import parse_return_event, ReturnEvent
from rental_return_events.response import create_failure_response, create_success_response
from rental_return_events.logger import log_function_calls

# ====================================================
# Rental Eligibility Helpers
# ====================================================

def rental_is_of_asset_type(asset_type: str, rental: Rental) -> bool:
    """Returns rentals with a specific asset type
    
    Args:
        asset_type (str): Asset type
        rental (Rental): Rental object 
    
    Returns:
        bool: True if the asset_type is one of the specified rental asset types
    """
    return asset_type in set(rental.eligible_asset_types)

def rental_is_non_expired(rental: Rental, timestamp: datetime) -> bool:
    """Returns rentals that are not expired

    Args:
        rental (Rental): Rental object
        timestamp (datetime): Current timestamp
    
    Returns:
        bool: True if the rental is not expired
    """
    return not rental.expires_at or datetime.fromisoformat(rental.expires_at) > timestamp

def fetch_valid_asset(asset_id: str) -> Optional[Asset]:
    """Fetches a valid asset from the database

    Args:
        asset_id (str): Asset ID
    
    Returns:
        Optional[Asset]: Asset object if found, None otherwise
    """
    try:
        return get_asset(asset_id)
    
    except (ValueError, TypeError) as e:
        print(f"Asset not found: {asset_id} | Error: {str(e)}")
        #logger.warning("Asset not found: %s | Error: %s", asset_id, str(e))
        raise LookupError(f"Asset not found: {asset_id}")

# ====================================================
# Find Eligible Rental
# ====================================================

def active_eligible_rentals(return_event: ReturnEvent) -> List[Rental]:
    """Returns rentals that are in progress, eligible, and not expired.
    
    Args:
        return_event (ReturnEvent): Return event object
    
    Returns:
        List[Rental]: List of eligible rentals
    """
    try:
        rentals = list_rentals_for_user(return_event.user_id)
        asset = fetch_valid_asset(return_event.asset_id)    

        return [
            rental for rental in rentals
            if rental.status == "IN_PROGRESS"
            and rental_is_of_asset_type(asset.asset_type, rental)
            and rental_is_non_expired(rental, return_event.timestamp)
        ]

    except LookupError:
        return []

@log_function_calls
def find_oldest_rental_from(rentals: List[Rental]) -> Optional[Rental]:
    """Finds the oldest rental
    
    Args:
        rentals (List[Rental]): List of rentals
    
    Returns:
        Optional[Rental]: Oldest rental if found, None otherwise
    """
    try:
        return min(rentals, key=lambda r: datetime.fromisoformat(r.created_at))
    except ValueError:  # min() raises ValueError on an empty list
        return None

# ====================================================
# Process Eligible Rental
# ====================================================
@log_function_calls
def finalize_rental_return(rental: Rental, return_event: ReturnEvent) -> Rental:
    """Finalizes the rental return

    Args:
        rental (Rental): Rental object
        return_event (ReturnEvent): Return event object
    
    Returns:
        Rental: Updated rental object
    """
    complete_rental(
        id=rental.id, 
        status="COMPLETED", 
        returned_at=return_event.timestamp.isoformat(), 
        returned_at_location_id=return_event.location_id
    )

    return get_rental(rental.id)

def complete_rental_return(return_event: ReturnEvent) -> dict:
    """Completes the oldest eligible rental for the user
    
    Args:
        return_event (ReturnEvent): Return event object
    
    Returns:
        dict: Rental return response
    """
    rental = find_oldest_rental_from(active_eligible_rentals(return_event))

    if not rental:
        return create_failure_response(f"No active rentals found for user {return_event.user_id}")    

    return create_success_response(finalize_rental_return(rental, return_event))

def process_rental_return(event: dict) -> dict:
    """Processe rental return events
    
    Args:
        event (dict): JSON event data
    
    Raises:
        ValueError: If the event data is invalid

    Returns:
        dict: Rental return response
    """
    try:
        return_event = parse_return_event(event)
        return complete_rental_return(return_event)
    
    except ValueError as e:
        return create_failure_response(f"Invalid return event: str(e)")
    
    except Exception as e:
        return create_failure_response(f"Error processing rental return: {str(e)}")
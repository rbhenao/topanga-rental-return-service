from tabulate import tabulate
from typing import List 

from dataclasses import dataclass, asdict
from typing import List, Optional
from topanga_queries.rentals import Rental

# Utilities for the return event application

# ====================================================
# Print Functions
# ====================================================
def debug_print(verbose_mode: bool, *args, **kwargs):
    """Prints debug logs if VERBOSE_MODE is enabled"""
    if verbose_mode:
        print(*args, **kwargs)

def debug_print_table(verbose_mode: bool, title: str, headers: List[str], data: List[List[str]]):
    """Prints a table in debug mode if VERBOSE_MODE is enabled"""
    if verbose_mode:
        print(f"\n{title}")
        print(tabulate(data, headers=headers, tablefmt="grid"))

def print_return_event(verbose_mode: bool, return_event):
    """Pretty prints the return event details in a table format."""
    headers = ["User ID", "Asset ID", "Location ID", "Timestamp"]
    data = [[return_event.user_id, return_event.asset_id, return_event.location_id, return_event.timestamp]]
    debug_print_table(verbose_mode, "RETURN EVENT PARSED:", headers, data)

def print_rental(verbose_mode: bool, rental: Rental, title: str):
    """Pretty prints the rental details in a table format."""
    headers = ["Rental ID", "User ID", "Asset ID", "Created At", "Expires At", "Status", "Eligible Asset Types"]
    data = [[rental.id, rental.user_id, rental.asset_id, rental.created_at, rental.expires_at, rental.status, rental.eligible_asset_types]]
    debug_print_table(verbose_mode, title, headers, data)


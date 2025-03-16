"""
Handler for processing rental return events.

This module contains helper functions for checking rental eligibility, 
processing return events, and finalizing rental returns.
"""
import base64
import binascii
from dataclasses import dataclass
from datetime import datetime

from rental_return_events.logger import log_function_calls


@dataclass
class ReturnEvent:
    """Represents a return event."""
    user_id: str
    asset_id: str
    location_id: str
    timestamp: datetime


def decode_qr(encoded_str: str) -> str:
    """Decodes base64 encoded QR

    Args:
        encoded_str (str): Base64 encoded string

    Raises:
        ValueError: If the string cannot be decoded

    Returns:
        str: Decoded string
    """
    try:
        return base64.b64decode(encoded_str).decode("utf-8")
    except (UnicodeDecodeError, binascii.Error) as e:
        raise ValueError(f"Could not decode QR: {str(e)}") from e


def convert_timestamp(timestamp: str) -> datetime:
    """Converts the timestamp to datetime object.

    Args:
        timestamp (str): ISO formatted timestamp

    Raises:
        ValueError: If the timestamp cannot be decoded

    Returns:
        datetime: Datetime object
    """
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError as e:
        raise ValueError(f"Invalid timestamp: {timestamp} | Error: {str(e)}") from e


@log_function_calls
def parse_return_event(event: dict) -> ReturnEvent:
    """Parses return event dict and returns a ReturnEvent object.

    Args:
        event (dict): JSON event data

    Raises:
        ValueError: If any required key is missing

    Returns:
        ReturnEvent: Parsed return event
    """
    required_keys = [
        "user_qr_data",
        "asset_qr_data",
        "location_id",
        "timestamp"]

    try:
        missing_keys = [key for key in required_keys if key not in event]
        if missing_keys:
            raise KeyError(f"Missing required keys: {', '.join(missing_keys)}")

        return ReturnEvent(
            user_id=decode_qr(event["user_qr_data"]),
            asset_id=decode_qr(event["asset_qr_data"]),
            location_id=event["location_id"],
            timestamp=convert_timestamp(event["timestamp"]),
        )

    except KeyError as e:
        raise KeyError(f"Missing event key(s): {str(e)}") from e

    except ValueError as e:
        raise ValueError(f"Failed to parse return event: {str(e)}") from e

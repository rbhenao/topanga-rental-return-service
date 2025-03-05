import base64
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class ReturnEvent:
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
    except Exception as e:
        raise ValueError(f"Could not decode QR: {str(e)}")

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
    except Exception as e:
        raise ValueError(f"Could not decode timestamp: {str(e)}")

def parse_return_event(event: dict) -> ReturnEvent:
    """Parses return event dict and returns a ReturnEvent object.

    Args:
        event (dict): JSON event data
    
    Raises:
        ValueError: If any required key is missing

    Returns:
        ReturnEvent: Parsed return event
    """
    try:
        user_id = decode_qr(event["user_qr_data"])
        asset_id = decode_qr(event["asset_qr_data"])
        location_id = event["location_id"]
        timestamp = convert_timestamp(event["timestamp"])

        if not user_id or not asset_id or not location_id or not timestamp:
            raise ValueError("Missing required event data")

        return ReturnEvent(user_id, asset_id, location_id, timestamp)

    except Exception as e:
        raise ValueError(f"Missing required event key: {str(e)}")
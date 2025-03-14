import logging
import sys
import functools
import json
from tabulate import tabulate

logger = logging.getLogger("rental_return_events")

def configure_logging(verbose=False):
    """Configures logging level based on verbose mode."""
    log_level = logging.DEBUG if verbose else logging.WARNING
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    
    # Clear existing handlers before adding new ones to prevent duplicates
    if not logger.handlers:
        logger.addHandler(console_handler)

def infer_object_type(obj):
    """Infers the type of an object based on its attributes."""
    if obj is None or isinstance(obj, (int, float, str, bool)):
        return None  # Skip primitives

    if isinstance(obj, dict):
        keys = obj.keys()
    elif hasattr(obj, "__dict__"):
        keys = obj.__dict__.keys()
    else:
        return None  # Skip unsupported types

    if {"user_id", "asset_id", "location_id", "timestamp"} <= keys:
        return "ReturnEvent"
    if {"id", "user_id", "asset_id", "created_at", "expires_at", "status", "eligible_asset_types"} <= keys:
        return "Rental"
    return None

def format_output(value):
    """Formats logging output based on data type."""
    if isinstance(value, dict):
        return json.dumps(value, indent=4)

    obj_type = infer_object_type(value)

    if obj_type == "ReturnEvent":
        headers = ["User ID", "Asset ID", "Location ID", "Timestamp"]
        data = [[value.user_id, value.asset_id, value.location_id, value.timestamp]]
        return "\nRETURN EVENT PARSED:\n" + tabulate(data, headers=headers, tablefmt="grid")

    if obj_type == "Rental":
        headers = ["Rental ID", "User ID", "Asset ID", "Created At", "Expires At", "Status", "Eligible Asset Types"]
        data = [[value.id, value.user_id, value.asset_id, value.created_at, value.expires_at, value.status, value.eligible_asset_types]]
        return "\nELIGIBLE RENTAL FOUND:\n" + tabulate(data, headers=headers, tablefmt="grid")

    if isinstance(value, list) and len(value) > 0:
        obj_type = infer_object_type(value[0])  # Check the first item
        if obj_type == "Rental":
            headers = ["Rental ID", "User ID", "Asset ID", "Created At", "Expires At", "Status", "Eligible Asset Types"]
            data = [[r.id, r.user_id, r.asset_id, r.created_at, r.expires_at, r.status, r.eligible_asset_types] for r in value]
            return "\nELIGIBLE RENTALS:\n" + tabulate(data, headers=headers, tablefmt="grid")

    return value

def log_function_calls(func):
    """Decorator to automatically log function calls and results."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if logger.isEnabledFor(logging.DEBUG):
            arg_str = ", ".join([repr(a) for a in args])
            kwarg_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
            logger.debug(f"CALL: {func.__name__}({arg_str}, {kwarg_str})")

        result = func(*args, **kwargs)

        if logger.isEnabledFor(logging.DEBUG):
            formatted_result = format_output(result)
            logger.debug(f"RETURN: {func.__name__} -> {formatted_result}")

        return result

    return wrapper
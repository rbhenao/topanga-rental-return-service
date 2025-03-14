import json
import os
import base64
from datetime import datetime, timezone, timedelta

REFERENCE_NOW = datetime(2025, 2, 10, 12, 0, 0, tzinfo=timezone.utc)


def encode_qr(data: str) -> str:
    """Encodes a string to Base64."""
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def generate_test_events():
    test_events = [
        {
            # "filename": "test_01_basic_return.json",
            "filename": "event_01.json",
            "data": {
                "timestamp": (REFERENCE_NOW + timedelta(hours=-1)).isoformat(),
                "location_id": "topanga-location-01",
                "user_qr_data": encode_qr("tpg_u0001"),
                "asset_qr_data": encode_qr("tpg_a00001"),
            },
            "description": "User tpg_u0001 returning the same asset they checked out (tpg_a00001).",
        },
        {
            # "filename": "test_02_multiple_rentals.json",
            "filename": "event_02.json",
            "data": {
                "timestamp": (REFERENCE_NOW + timedelta(minutes=30)).isoformat(),
                "location_id": "topanga-location-02",
                "user_qr_data": encode_qr("tpg_u0002"),
                "asset_qr_data": encode_qr("tpg_a00015"),
            },
            "description": "User tpg_u0002 returning one of their multiple active rentals (tpg_a00015).",
        },
        {
            # "filename": "test_03_invalid_return.json",
            "filename": "event_03.json",
            "data": {
                "timestamp": (REFERENCE_NOW + timedelta(hours=1)).isoformat(),
                "location_id": "topanga-location-03",
                "user_qr_data": encode_qr("tpg_u0005"),
                "asset_qr_data": encode_qr("tpg_a00500"),  # Invalid asset
            },
            "description": "User tpg_u0005 attempting to return an asset they never rented (invalid).",
        },
        {
            # "filename": "test_04_expired_rental.json",
            "filename": "event_04.json",
            "data": {
                "timestamp": (REFERENCE_NOW + timedelta(hours=2)).isoformat(),
                "location_id": "topanga-location-01",
                "user_qr_data": encode_qr("tpg_u0004"),
                "asset_qr_data": encode_qr("tpg_a00025"),
            },
            "description": "User tpg_u0004 returning an asset, check if rental is expired before updating.",
        },
        {
            # "filename": "test_05_eligible_asset_type.json",
            "filename": "event_05.json",
            "data": {
                "timestamp": (REFERENCE_NOW + timedelta(hours=3)).isoformat(),
                "location_id": "topanga-location-01",
                "user_qr_data": encode_qr("tpg_u0001"),
                "asset_qr_data": encode_qr("tpg_a00002"),  # Different but eligible type
            },
            "description": "User tpg_u0001 returning an asset of a different but eligible type (clamshell instead of 3-compartment).",
        },
    ]

    os.makedirs("example_events", exist_ok=True)

    for event in test_events:
        file_path = os.path.join("example_events", event["filename"])
        with open(file_path, "w") as f:
            json.dump(event["data"], f, indent=4)

        print(f"Saved: {file_path} - {event['description']}")


if __name__ == "__main__":
    generate_test_events()

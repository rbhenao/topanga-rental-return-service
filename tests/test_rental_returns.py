import pytest
import json
from datetime import datetime, timezone

from topanga_queries.rentals import Rental

from rental_return_events.return_event_received import *
from rental_return_events.return_event_response import *
from rental_return_events.process_rental_return import *

# =========================
# return_event_received.py
# =========================

def test_decode_qr():
    """Test if the QR decoding function works as expected."""

    user_qr_data = "dHBnX3UwMDAx"
    asset_qr_data = "dHBnX2EwMDAwMQ=="

    expected_user_qr_data="tpg_u0001"
    expected_asset_qr_data="tpg_a00001"

    assert decode_qr(user_qr_data) == expected_user_qr_data
    assert decode_qr(asset_qr_data) == expected_asset_qr_data

def test_convert_timestamp():
    """Test timestamp conversion function works as expected."""

    timestamp = "2025-02-10T11:00:00+00:00"
    expected = datetime(2025, 2, 10, 11, 0, 0, tzinfo=timezone.utc)

    assert convert_timestamp(timestamp) == expected

def test_parse_return_event():
    """Test parsing return event."""
    
    event = {
        "timestamp": "2025-02-10T11:00:00+00:00",
        "location_id": "topanga-location-01",
        "user_qr_data": "dHBnX3UwMDAx",
        "asset_qr_data": "dHBnX2EwMDAwMQ=="
    }
    
    expected = ReturnEvent(
        user_id="tpg_u0001",
        asset_id="tpg_a00001",
        location_id="topanga-location-01",
        timestamp=datetime(2025, 2, 10, 11, 0, 0, tzinfo=timezone.utc),
    )

    parsed_event = parse_return_event(event)
    
    assert parsed_event == expected

# =========================-
# return_event_response.py
# =========================

def test_create_success_response():
    """Test the success response function."""
    
    rental = Rental(
        id='2152d14c-708d-4053-9f3f-246fd472f1aa', 
        user_id='tpg_u0001', 
        asset_id='tpg_a00001', 
        created_at_location_id='topanga-location-01', 
        created_at='2025-02-05T12:00:00+00:00', 
        expires_at='2025-02-15T12:00:00+00:00', 
        status='COMPLETED', 
        eligible_asset_types='["3-compartment", "clamshell"]', 
        returned_at_location_id='topanga-location-01', 
        returned_at='2025-02-10T11:00:00+00:00'
    )

    verbose_mode = False

    expected = {
        "status": "SUCCESS",
        "message": "Rental successfully completed",
        "rental_id": "2152d14c-708d-4053-9f3f-246fd472f1aa",
        "rental_returned_at": "2025-02-10T11:00:00+00:00",
        "rental_status": "COMPLETED",
        "error": None
    }

    result = create_success_response(rental, verbose_mode)

    assert result == expected

def test_create_failure_response():
    """Test the failure response function."""
    
    message = "No eligible rental found"

    expected = {
        "status": "FAILED",
        "message": "No eligible rental found",
        "rental_id": None,
        "rental_returned_at": None,
        "rental_status": None,
        "error": "No eligible rental found"
    }

    result = create_failure_response(message)

    assert result == expected

# =========================-
# process_rental_return.py
# =========================

def test_rental_is_of_asset_type():
    """Test the asset type function."""
    rental = Rental(
        id='2152d14c-708d-4053-9f3f-246fd472f1aa', 
        user_id='tpg_u0001', 
        asset_id='tpg_a00001', 
        created_at_location_id='topanga-location-01', 
        created_at='2025-02-05T12:00:00+00:00', 
        expires_at='2025-02-15T12:00:00+00:00', 
        status='IN_PROGRESS', 
        eligible_asset_types='["3-compartment", "clamshell"]', 
        returned_at_location_id=None, 
        returned_at=None) 
    
    asset_type = "3-compartment"
    
    result = rental_is_of_asset_type(asset_type, rental)

    assert result

def test_rental_is_non_expired():
    """Test the non expired rental function."""
    rental = Rental(
        id='2152d14c-708d-4053-9f3f-246fd472f1aa', 
        user_id='tpg_u0001', 
        asset_id='tpg_a00001', 
        created_at_location_id='topanga-location-01', 
        created_at='2025-02-05T12:00:00+00:00', 
        expires_at='2025-02-15T12:00:00+00:00', 
        status='IN_PROGRESS', 
        eligible_asset_types='["3-compartment", "clamshell"]', 
        returned_at_location_id=None, 
        returned_at=None) 

    timestamp = datetime.fromisoformat('2025-02-10T11:00:00+00:00')

    result = rental_is_non_expired(rental, timestamp)

    assert result

def test_fetch_valid_asset():
    """Test the fetch valid asset function."""

    asset_id1 = "tpg_a00001"
    asset_id2 = "tpg_a00002"
    asset_id3 = "tpg_a00003"

    result1 = fetch_valid_asset(asset_id1)
    result2 = fetch_valid_asset(asset_id2)
    result3 = fetch_valid_asset(asset_id3)

    assert result1.asset_type == "clamshell"
    assert result2.asset_type == "large-bowl"
    assert result3.asset_type == "small-bowl"

def test_active_eligible_rentals(load_event):
    """Test the active eligible rentals function."""

    event_01 = parse_return_event(load_event("event_01.json"))

    result = active_eligible_rentals(event_01)

    assert len(result) == 1
    assert result[0].asset_id == "tpg_a00001"
    assert "3-compartment" in result[0].eligible_asset_types
    assert "clamshell" in result[0].eligible_asset_types

def test_find_oldest_rental_from():
    """Test the find oldest rental function."""

    rentals = [
        Rental(
            id='2152d14c-708d-4053-9f3f-246fd472f1aa', 
            user_id='tpg_u0001', 
            asset_id='tpg_a00001', 
            created_at_location_id='topanga-location-01', 
            created_at='2025-02-05T12:00:00+00:00', 
            expires_at='2025-02-15T12:00:00+00:00', 
            status='IN_PROGRESS', 
            eligible_asset_types='["3-compartment", "clamshell"]', 
            returned_at_location_id=None, 
            returned_at=None), 
        Rental(
            id='814404a3-89bf-4df1-b2f3-8d92acaf6b40', 
            user_id='tpg_u0001', 
            asset_id='tpg_a00002', 
            created_at_location_id='topanga-location-01', 
            created_at='2025-02-07T12:00:00+00:00', 
            expires_at='2025-02-14T12:00:00+00:00', 
            status='IN_PROGRESS', 
            eligible_asset_types='["large-bowl", "small-bowl"]', 
            returned_at_location_id=None, 
            returned_at=None
        )
    ]

    result = find_oldest_rental_from(rentals)

    assert result.id == "2152d14c-708d-4053-9f3f-246fd472f1aa"

def test_complete_rental_return01(load_event):
    """Test the complete rental function."""

    event_01 = load_event("event_01.json")
    return_event = parse_return_event(event_01)
    result = complete_rental_return(return_event)

    assert result["rental_status"] == "COMPLETED"

def test_complete_rental_return02(load_event):
    """Test the complete rental function."""

    event_02 = load_event("event_02.json")
    return_event = parse_return_event(event_02)
    result = complete_rental_return(return_event)

    assert result["rental_status"] == "COMPLETED"

# should return None as 03 returns no valid rental
def test_complete_rental_return03(load_event):
    """Test the complete rental function."""

    event_03 = load_event("event_03.json")
    return_event = parse_return_event(event_03)
    result = complete_rental_return(return_event)

    assert result["rental_status"] == None

def test_complete_rental_return04(load_event):
    """Test the complete rental function."""

    event_04 = load_event("event_04.json")
    return_event = parse_return_event(event_04)
    result = complete_rental_return(return_event)

    assert result["rental_status"] == "COMPLETED"

def test_complete_rental_return05(load_event):
    """Test the complete rental function."""

    event_05 = load_event("event_05.json")
    return_event = parse_return_event(event_05)
    result = complete_rental_return(return_event)

    assert result["rental_status"] == "COMPLETED"

def test_process_rental_return(load_event):
    """Test if the rental return process runs without errors."""

    event_01 = load_event("event_01.json")
    process_rental_return(event_01)

    assert True
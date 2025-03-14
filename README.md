# **Topanga Rental Return Service**
This service handles rental return events for **ReusePass**, supporting sustainability through reusable packaging.

## High-Level Overview
- The service takes a json payload and returns a json payload
- The input payload is parsed as a **ReturnEvent** in **`handler.py`**
- **ReturnEvent** is then processed in **`processor.py`**
- Finally a **RentalReturnResponse** output payload is created and returned in **`response.py`**

## Engineering Choices
- **Event-Driven:** The service processes return events asychronously in order to not block other microservices
- **Strict JSON Schema:** The service ensure consistent response structure to be easily used by downstream services
- **Modular design:** logic for parsing, processing and responding in separate modules
- **Dependency Management:** use pip and venv to ensure consistent environment

---

**Output**
Because this service is intended to be used by downstream services, it is important to have a predictable structured output.
We model this with a RentalReturnResponse Object:

**SUCCESS**
```json
{
    "status": "SUCCESS",
    "message": "Rental successfully completed",
    "rental_id": "b5bc2838-b0ba-4fb8-94fc-21da32f41747",
    "rental_returned_at": "2025-02-10T11:00:00+00:00",
    "rental_status": "COMPLETED",
    "error": null
}
```

**FAILURE**
```json
{
    "status": "FAILED",
    "message": "No active rentals found for user tpg_u0001",
    "rental_id": null,
    "rental_returned_at": null,
    "rental_status": null,
    "error": "No eligible rental found"
}
```
## Handling Downstream Side-Effects
Some side effects that can be triggered and implemented via SNS and SQS...
- SNS notifications to users once a rental is completed
- Enqueue our RentalReturnResponse object to an SQS queue
- We can have a success queue and a failure queue
- Microservices process the queues to take actions from there (user status update, reward system updates, alerting on failures)
---

## TODOs For Production
Some of the changes needed to make the service production ready...
- Add more robust error checking at all stages of return event processing
- Add specific error messages to the response for each type of error e.g. invalid asset, invalid user, rental expired.
- More detailed unit tests (not just testing happy paths)
- Add authentication and authorization checking
- Add retries for transient database issues
- Add CI/CD pipeline with GitHub Actions
- Make adjustments to run smoothly on AWS Lambda in cloud environment
- Event deduplication strategies with idempotency checks in database
- Add detailed logging and monitoring
---

### Cloud Architecture Diagram 

#### *For a Cloud Architecture Diagram see `./Documentation/architecture.png`*

---

## **Setup Instructions**
### **1. Create Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate
```

### **2️. Install Dependencies**
*two separate pip installs for each package*
```sh
cd topanga_queries
pip install -e .
```

```sh
cd rental_return_events
pip install -e .
```

### **3. Initialize the Database**
```sh
cd rental_return_events
python -m topanga_queries.bootstrap.db
```

---

## **Running the Rental Return Service**
### **Basic Usage**
*Run from rental_return_events (package level not nested) dir!*
```sh
cd rental_return_events
python -m rental_return_events.main ../topanga_queries/example_events/event_01.json
```
### **Example Output**
```json
{
    "status": "SUCCESS",
    "message": "Rental successfully completed",
    "rental_id": "768770ac-a2df-4145-b722-80e57984fb11",
    "rental_returned_at": "2025-02-10T15:00:00+00:00",
    "rental_status": "COMPLETED",
    "error": null
}
```

---

## **Example 2 (Verbose Mode)**
```sh
python -m rental_return_events.main ../topanga_queries/example_events/event_01.json --verbose
```

#### **Output:**
```
2025-03-13 18:49:30 - rental_return_events - DEBUG - CALL: parse_return_event({'timestamp': '2025-02-10T11:00:00+00:00', 'location_id': 'topanga-location-01', 'user_qr_data': 'dHBnX3UwMDAx', 'asset_qr_data': 'dHBnX2EwMDAwMQ=='}, )
2025-03-13 18:49:30 - rental_return_events - DEBUG - RETURN: parse_return_event -> 
RETURN EVENT PARSED:
+-----------+------------+---------------------+---------------------------+
| User ID   | Asset ID   | Location ID         | Timestamp                 |
+===========+============+=====================+===========================+
| tpg_u0001 | tpg_a00001 | topanga-location-01 | 2025-02-10 11:00:00+00:00 |
+-----------+------------+---------------------+---------------------------+
2025-03-13 18:49:30 - rental_return_events - DEBUG - CALL: find_oldest_rental_from([Rental(id='eea6c617-9c44-45be-8b66-5c868a64ab7d', user_id='tpg_u0001', asset_id='tpg_a00001', created_at_location_id='topanga-location-01', created_at='2025-02-05T12:00:00+00:00', expires_at='2025-02-15T12:00:00+00:00', status='IN_PROGRESS', eligible_asset_types=['3-compartment', 'clamshell'], returned_at_location_id=None, returned_at=None)], )
2025-03-13 18:49:30 - rental_return_events - DEBUG - RETURN: find_oldest_rental_from -> 
ELIGIBLE RENTAL FOUND:
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-------------+--------------------------------+
| Rental ID                            | User ID   | Asset ID   | Created At                | Expires At                | Status      | Eligible Asset Types           |
+======================================+===========+============+===========================+===========================+=============+================================+
| eea6c617-9c44-45be-8b66-5c868a64ab7d | tpg_u0001 | tpg_a00001 | 2025-02-05T12:00:00+00:00 | 2025-02-15T12:00:00+00:00 | IN_PROGRESS | ['3-compartment', 'clamshell'] |
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-------------+--------------------------------+
2025-03-13 18:49:30 - rental_return_events - DEBUG - CALL: finalize_rental_return(Rental(id='eea6c617-9c44-45be-8b66-5c868a64ab7d', user_id='tpg_u0001', asset_id='tpg_a00001', created_at_location_id='topanga-location-01', created_at='2025-02-05T12:00:00+00:00', expires_at='2025-02-15T12:00:00+00:00', status='IN_PROGRESS', eligible_asset_types=['3-compartment', 'clamshell'], returned_at_location_id=None, returned_at=None), ReturnEvent(user_id='tpg_u0001', asset_id='tpg_a00001', location_id='topanga-location-01', timestamp=datetime.datetime(2025, 2, 10, 11, 0, tzinfo=datetime.timezone.utc)), )
2025-03-13 18:49:30 - rental_return_events - DEBUG - RETURN: finalize_rental_return -> 
ELIGIBLE RENTAL FOUND:
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-----------+--------------------------------+
| Rental ID                            | User ID   | Asset ID   | Created At                | Expires At                | Status    | Eligible Asset Types           |
+======================================+===========+============+===========================+===========================+===========+================================+
| eea6c617-9c44-45be-8b66-5c868a64ab7d | tpg_u0001 | tpg_a00001 | 2025-02-05T12:00:00+00:00 | 2025-02-15T12:00:00+00:00 | COMPLETED | ['3-compartment', 'clamshell'] |
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-----------+--------------------------------+
{
    "status": "SUCCESS",
    "message": "Rental successfully completed",
    "rental_id": "eea6c617-9c44-45be-8b66-5c868a64ab7d",
    "rental_returned_at": "2025-02-10T11:00:00+00:00",
    "rental_status": "COMPLETED",
    "error": null
}
```

---

## **Running Tests**
```sh
cd rental_return_events
pytest tests/ -v
```
---

## **Notes**
- **Verbose Mode** (`--verbose`) provides detailed logs for debugging.
- **Ensure database initialization** (`topanga_queries/bootstrap/db.py`) is run before using the service.
- **Tests should be run inside the `tests/` directory** using `pytest`.

---

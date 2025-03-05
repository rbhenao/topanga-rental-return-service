# **Topanga Rental Return Service**
This service handles rental return events for **ReusePass**, supporting sustainability through reusable packaging.

## High-Level Overview
- The service takes a json payload and returns a json payload
- The input payload is parsed as a **ReturnEvent** in **`return_event_received.py`**
- **ReturnEvent** is then processed in **`process_rental_return.py`**
- Finally a **RentalReturnResponse** output payload is created and returned in **`return_event_response.py`**

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
*two separate pip installs for now to avoid changing topanga package*
```sh
pip install -r requirements.txt
```

```sh
cd src
pip install -e .
```

### **3. Initialize the Database**
```sh
python topanga_queries/bootstrap/db.py
```

---

## **Running the Rental Return Service**
### **Basic Usage**
*(Note! Needs to run from src dir) TODO: update to run from anywhere*
```sh
cd src
python rental_returns.py example_events/event_05.json
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
python rental_returns.py example_events/event_05.json --verbose
```
#### **Output:**
```
Received Return Event JSON:
{
    "timestamp": "2025-02-10T15:00:00+00:00",
    "location_id": "topanga-location-01",
    "user_qr_data": "dHBnX3UwMDAx",
    "asset_qr_data": "dHBnX2EwMDAwMg=="
}

Return Event Parsed:
+-----------+------------+---------------------+---------------------------+
| User ID   | Asset ID   | Location ID         | Timestamp                 |
+===========+============+=====================+===========================+
| tpg_u0001 | tpg_a00002 | topanga-location-01 | 2025-02-10 15:00:00+00:00 |
+-----------+------------+---------------------+---------------------------+

Eligible Rental Found:
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-------------+------------------------------+
| Rental ID                            | User ID   | Asset ID   | Created At                | Expires At                | Status      | Eligible Asset Types         |
+======================================+===========+============+===========================+===========================+=============+==============================+
| 768770ac-a2df-4145-b722-80e57984fb11 | tpg_u0001 | tpg_a00002 | 2025-02-07T12:00:00+00:00 | 2025-02-14T12:00:00+00:00 | IN_PROGRESS | ['large-bowl', 'small-bowl'] |
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-------------+------------------------------+

Updated Rental:
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-----------+------------------------------+
| Rental ID                            | User ID   | Asset ID   | Created At                | Expires At                | Status    | Eligible Asset Types         |
+======================================+===========+============+===========================+===========================+===========+==============================+
| 768770ac-a2df-4145-b722-80e57984fb11 | tpg_u0001 | tpg_a00002 | 2025-02-07T12:00:00+00:00 | 2025-02-14T12:00:00+00:00 | COMPLETED | ['large-bowl', 'small-bowl'] |
+--------------------------------------+-----------+------------+---------------------------+---------------------------+-----------+------------------------------+

Final Rental Completion Response:
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

## **Running Tests**
```sh
cd tests
pytest -v
```
---

## **Notes**
- **Verbose Mode** (`--verbose`) provides detailed logs for debugging.
- **Ensure database initialization** (`topanga_queries/bootstrap/db.py`) is run before using the service.
- **Tests should be run inside the `tests/` directory** using `pytest`.

---

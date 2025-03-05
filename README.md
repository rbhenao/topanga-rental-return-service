# **Topanga Rental Return Service**
This service handles rental return events for **ReusePass**.

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

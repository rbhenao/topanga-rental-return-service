import json
import base64
import sys
import os

from rental_return_events.process_rental_return import process_rental_return
from topanga_queries.bootstrap.db import initialize_challenge_db

# Global flag to enable verbose logging
global VERBOSE_MODE
VERBOSE_MODE = False

def load_json_file(file_path):
    """Loads the JSON file and return its contents as dictionary."""
    
    if not os.path.exists(file_path): 
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <event_file.json> [--verbose]")
        sys.exit(1)
    
    # Check for optional --verbose flag
    VERBOSE_MODE = "--verbose" in sys.argv

    json_file = sys.argv[1] # read the json return event file
    
    try:
        # Read JSON payload and complete the return event 
        payload = load_json_file(json_file)
        response = process_rental_return(payload, VERBOSE_MODE)
        print(json.dumps(response, indent=4)) # Print structured JSON response
    except Exception as e:
        print(f"Error processing return event: {str(e)}")
        sys.exit(1)
    
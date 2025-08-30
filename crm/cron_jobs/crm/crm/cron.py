from datetime import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """Log a heartbeat message every 5 minutes."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # (اختياري) اختبار GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"{timestamp} GraphQL hello OK")
        else:
            print(f"{timestamp} GraphQL error: {response.status_code}")
    except Exception as e:
        print(f"{timestamp} GraphQL request failed: {e}")

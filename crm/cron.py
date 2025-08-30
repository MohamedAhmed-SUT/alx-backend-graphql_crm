from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """Log a heartbeat message and check GraphQL hello field."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # تحقق من GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        print(f"{timestamp} GraphQL hello: {result.get('hello')}")
    except Exception as e:
        print(f"{timestamp} GraphQL request failed: {e}")

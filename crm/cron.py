from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOW_STOCK_LOG = "/tmp/low_stock_updates_log.txt"
HEARTBEAT_LOG = "/tmp/crm_heartbeat_log.txt"


def update_low_stock():
    """Run GraphQL mutation to restock low-stock products and log results."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql(
            """
            mutation {
                updateLowStockProducts {
                    success
                    products {
                        name
                        stock
                    }
                }
            }
            """
        )

        result = client.execute(mutation)
        updates = result["updateLowStockProducts"]["products"]

        with open(LOW_STOCK_LOG, "a") as f:
            for p in updates:
                f.write(f"{timestamp} - {p['name']} restocked to {p['stock']}\n")

        print("Low stock update processed!")

    except Exception as e:
        with open(LOW_STOCK_LOG, "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")
        print(f"Error: {e}")


def log_crm_heartbeat():
    """Logs a heartbeat entry with timestamp to /tmp/crm_heartbeat_log.txt."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HEARTBEAT_LOG, "a") as f:
        f.write(f"{now} - CRM heartbeat\n")

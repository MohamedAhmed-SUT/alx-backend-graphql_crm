#!/usr/bin/env python3
import sys
import asyncio
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"

async def main():
    # إعداد الاتصال مع GraphQL endpoint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # حساب التاريخ من 7 أيام
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # الاستعلام
    query = gql(
        """
        query GetRecentOrders($since: Date!) {
            orders(orderDate_Gte: $since) {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    # تنفيذ الاستعلام
    result = await client.execute_async(query, variable_values={"since": seven_days_ago})
    orders = result.get("orders", [])

    # تسجيل النتائج في اللوج
    with open(LOG_FILE, "a") as f:
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - Order {order_id}, Email: {email}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

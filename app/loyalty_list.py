"""
loyalty_list.py

Fetch all loyalty accounts from Square using cursor pagination
and print the loyalty account ID and associated customer ID.
"""

import json

from app.client import client
from square.core.api_error import ApiError


def loyalty_accounts_search() -> list[dict]:
    """Fetch loyalty account records and print their IDs."""
    cursor = None
    records = []
    count = 0

    while True:
        try:
            result = client.loyalty.accounts.search(cursor=cursor)
        except ApiError as error:
            errors = error.body.get("errors", [])

            if errors and errors[0].get("detail") == "Merchant does not have a loyalty program":
                print("No loyalty program is configured for this merchant yet.")
                break

            print("Loyalty accounts search failed.")
            print(error)
            break

        if result.errors:
            print("Loyalty accounts search failed.")
            print(result.errors)
            break

        if not result.loyalty_accounts:
            break

        for acct in result.loyalty_accounts:
            loyalty_id = acct.id
            customer_id = acct.customer_id or "NO_CUSTOMER"

            records.append(
                {
                    "loyalty_account_id": loyalty_id,
                    "customer_id": customer_id,
                }
            )

            count += 1

            print(f"loyalty_id: {loyalty_id}, customer_id: {customer_id}")
            print(f"processed {count} accounts")

        cursor = result.cursor

        if cursor is None:
            break

    return records


if __name__ == "__main__":
    records = loyalty_accounts_search()
    print(json.dumps(records, indent=2))

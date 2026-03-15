import json

from app.client import client
from square.core.api_error import ApiError

LOYALTY_ACCOUNT_ID = "ad026a62-f825-4927-98a1-4e093bc9ea6f"


def get_loyalty_account_by_id(loyalty_account_id: str) -> dict | None:
    """Search loyalty accounts and return the matching account as JSON-ready data."""
    cursor = None

    while True:
        try:
            result = client.loyalty.accounts.search(cursor=cursor)
        except ApiError as error:
            print("Loyalty account lookup failed.")
            print(error)
            return None

        if result.errors:
            print("Loyalty account lookup failed.")
            print(result.errors)
            return None

        if not result.loyalty_accounts:
            return None

        for account in result.loyalty_accounts:
            if account.id == loyalty_account_id:
                return account.model_dump()

        cursor = result.cursor
        if cursor is None:
            return None


if __name__ == "__main__":
    loyalty_account = get_loyalty_account_by_id(LOYALTY_ACCOUNT_ID)
    if loyalty_account is None:
        print(f"No loyalty account found for {LOYALTY_ACCOUNT_ID}.")
    else:
        print(json.dumps(loyalty_account, indent=2))

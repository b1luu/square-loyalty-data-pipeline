import json
import uuid

from app.client import client
from square.core.api_error import ApiError

CUSTOMER_ID = "J42RRWSJYDP85FKFD046MSRTV4"


def get_location() -> dict | None:
    """Return the first available sandbox location."""
    try:
        result = client.locations.list()
    except ApiError as error:
        print("Location lookup failed.")
        print(error)
        return None

    if result.errors:
        print("Location lookup failed.")
        print(result.errors)
        return None

    if not result.locations:
        print("No locations returned for this sandbox merchant.")
        return None

    location = result.locations[0]
    return location.model_dump()


def create_order() -> dict | None:
    """Create one small sandbox order for the test customer."""
    location = get_location()
    if location is None:
        return None

    currency = location.get("currency") or "USD"

    try:
        result = client.orders.create()
    except ApiError as error:
        print("Order creation failed.")
        print(error)
        return None

    if result.errors:
        print("Order creation failed.")
        print(result.errors)
        return None

    if result.order is None:
        print("Order creation returned no order.")
        return None

    return result.order.model_dump()


if __name__ == "__main__":
    order = create_order()
    if order:
        print(json.dumps(order, indent=2))

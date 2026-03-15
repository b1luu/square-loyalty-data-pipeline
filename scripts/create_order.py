import json
import uuid

from app.client import client
from square.core.api_error import ApiError

CUSTOMER_ID = "J42RRWSJYDP85FKFD046MSRTV4"
ITEM_VARIATION_ID = "CHHS3A7R27XN43JR2F5SR6CI"
ICE_MODIFIER_ID = "TE4FKPMJ5C4VJ74325ARVYPH"  # 50% Ice
SUGAR_MODIFIER_ID = "EOL2MQIK7OSHSQFKRN6AN4U6"  # 50% Sugar
TOPPING_MODIFIER_ID = "GHW2LHGIXP543X3LD5LFGEKH"  # Boba


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
    """Create one catalog-backed sandbox order for the test customer."""
    location = get_location()
    if location is None:
        return None

    try:
        result = client.orders.create(
            idempotency_key=str(uuid.uuid4()),
            order={
                "location_id": location["id"],
                "customer_id": CUSTOMER_ID,
                "reference_id": "sandbox-loyalty-order-1",
                "line_items": [
                    {
                        "catalog_object_id": ITEM_VARIATION_ID,
                        "quantity": "1",
                        "modifiers": [
                            {"catalog_object_id": ICE_MODIFIER_ID},
                            {"catalog_object_id": SUGAR_MODIFIER_ID},
                            {"catalog_object_id": TOPPING_MODIFIER_ID},
                        ],
                    }
                ],
            },
        )
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

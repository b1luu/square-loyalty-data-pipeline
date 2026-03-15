import json
import uuid

from app.client import client
from square.core.api_error import ApiError


def create_customer() -> dict | None:
    """Create one sandbox customer and return the created record."""
    try:
        result = client.customers.create(
            idempotency_key=str(uuid.uuid4()),
            given_name="Test",
            family_name="LoyaltyCustomer1",
            email_address="test.loyalty.customer1@example.com",
            phone_number="+14255550101",
            note="Sandbox customer created for loyalty and orders testing.",
        )
    except ApiError as error:
        print("Customer creation failed.")
        print(error)
        return None

    if result.errors:
        print("Customer creation failed.")
        print(result.errors)
        return None

    if result.customer is None:
        print("Customer creation returned no customer record.")
        return None

    return result.customer.model_dump()

if __name__ == "__main__":
    customer = create_customer()
    if customer:
        print(json.dumps(customer, indent=2))

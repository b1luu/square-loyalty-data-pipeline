import json 
import uuid

from app.client import client
from square.core.api_error import ApiError

result = client.loyalty.accounts.create(
    idempotency_key=str(uuid.uuid4()),
    loyalty_account={
        "program_id": "...",
        "customer_id": "...",
        "mapping": {
            "phone_number": "...",
        },
    },
)

print(json.dumps(result.loyalty_account.model_dump(), indent=2))

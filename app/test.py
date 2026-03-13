import os

from square import Square
from square.environment import SquareEnvironment


client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=os.environ["ACCESS_TOKEN"],
)

cursor = None

while True:
    result = client.loyalty.accounts.search(cursor=cursor)

    for acct in result.loyalty_accounts:
        loyalty_id = acct.id
        customer_id = acct.customer_id or "NO_CUSTOMER"

        print(f"loyalty_id:{loyalty_id},customer_id:{customer_id}")

    cursor = result.cursor

    if cursor is None:
        break
import os

from square import Square
from square.environment import SquareEnvironment


client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=os.environ["ACCESS_TOKEN"],
)

cursor = None
count = 0
while True:
    result = client.loyalty.accounts.search(cursor=cursor)

    if result.loyalty_accounts is None:
        print("No loyalty accounts returned. Stopping after {count} accounts.")
        break

    for acct in result.loyalty_accounts:
        loyalty_id = acct.id
        customer_id = acct.customer_id or "NO_CUSTOMER"
        count += 1 

        print(f"loyalty_id:{loyalty_id},customer_id:{customer_id}")
        print(f"processed {count} accounts")

    cursor = result.cursor

    if cursor is None:
        break


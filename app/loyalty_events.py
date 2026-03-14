import json

from client import client


def search_loyalty_events() -> list[dict]:
    cursor = None
    records = []
    count = 0

    while True:
        results = client.loyalty.search_events(cursor=cursor)

        if results.errors:
            print("Searching loyalty events failed.")
            print(results.errors)
            break

        if not results.events:
            break

        for event in results.events:
            loyalty_event_id = event.id
            loyalty_account_id = event.loyalty_account_id
            event_type = event.type
            created_at = event.created_at

            records.append(
                {
                    "loyalty_event_id": loyalty_event_id,
                    "loyalty_account_id": loyalty_account_id,
                    "event_type": event_type,
                    "created_at": created_at,
                }
            )

            count += 1

            print(
                f"loyalty_event_id: {loyalty_event_id}, "
                f"loyalty_account_id: {loyalty_account_id}"
            )
            print(f"processed {count} events")

        cursor = results.cursor

        if cursor is None:
            break

    return records


if __name__ == "__main__":
    records = search_loyalty_events()
    print(json.dumps(records, indent=2))

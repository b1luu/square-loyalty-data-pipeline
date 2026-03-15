import csv
from datetime import datetime
from pathlib import Path

from app.client import client
from square.core.api_error import ApiError

OUTPUT_PATH = Path("data/exports/loyalty_activity.csv")
CSV_COLUMNS = [
    "Date",
    "Time",
    "Category",
    "Item",
    "Qty",
    "Customer ID",
    "Loyalty_Member ID",
    "Order ID",
    "Event ID",
]


def fetch_loyalty_account_map() -> dict[str, str | None]:
    """Return loyalty_account_id -> customer_id."""
    cursor = None
    records = {}

    while True:
        try:
            result = client.loyalty.accounts.search(cursor=cursor)
        except ApiError as error:
            print("Loyalty accounts search failed.")
            print(error)
            return records

        if result.errors:
            print("Loyalty accounts search failed.")
            print(result.errors)
            return records

        if not result.loyalty_accounts:
            return records

        for account in result.loyalty_accounts:
            records[account.id] = account.customer_id

        cursor = result.cursor
        if cursor is None:
            return records


def extract_order_id(event) -> str | None:
    """Return the related order_id when the loyalty event exposes one."""
    if event.accumulate_points and event.accumulate_points.order_id:
        return event.accumulate_points.order_id

    if (
        event.accumulate_promotion_points
        and event.accumulate_promotion_points.order_id
    ):
        return event.accumulate_promotion_points.order_id

    if event.redeem_reward and event.redeem_reward.order_id:
        return event.redeem_reward.order_id

    return None


def fetch_loyalty_events_with_orders() -> list[dict]:
    cursor = None
    records = []

    while True:
        try:
            result = client.loyalty.search_events(cursor=cursor)
        except ApiError as error:
            print("Searching loyalty events failed.")
            print(error)
            return records

        if result.errors:
            print("Searching loyalty events failed.")
            print(result.errors)
            return records

        if not result.events:
            return records

        for event in result.events:
            order_id = extract_order_id(event)
            if order_id is None:
                continue

            records.append(
                {
                    "event_id": event.id,
                    "loyalty_account_id": event.loyalty_account_id,
                    "order_id": order_id,
                    "event_created_at": event.created_at,
                }
            )

        cursor = result.cursor
        if cursor is None:
            return records


def fetch_orders(order_ids: set[str]) -> dict[str, dict]:
    records = {}

    for order_id in sorted(order_ids):
        try:
            result = client.orders.get(order_id)
        except ApiError as error:
            print(f"Order lookup failed for {order_id}.")
            print(error)
            continue

        if result.errors:
            print(f"Order lookup failed for {order_id}.")
            print(result.errors)
            continue

        if result.order is None:
            continue

        records[order_id] = result.order.model_dump()

    return records


def fetch_category_map(variation_ids: set[str]) -> dict[str, str]:
    if not variation_ids:
        return {}

    try:
        result = client.catalog.batch_get(
            object_ids=sorted(variation_ids),
            include_related_objects=True,
            include_category_path_to_root=True,
        )
    except ApiError as error:
        print("Catalog lookup failed.")
        print(error)
        return {}

    if result.errors:
        print("Catalog lookup failed.")
        print(result.errors)
        return {}

    item_by_id = {}

    for obj in (result.related_objects or []):
        if obj.type == "ITEM" and obj.item_data:
            item_by_id[obj.id] = obj.item_data

    category_ids = set()
    for item_data in item_by_id.values():
        category_ids.update(extract_category_ids(item_data))

    category_by_id = fetch_categories_by_id(category_ids)

    category_map = {}

    for obj in (result.objects or []):
        if obj.type != "ITEM_VARIATION" or obj.item_variation_data is None:
            continue

        item_data = item_by_id.get(obj.item_variation_data.item_id)
        if item_data is None:
            continue

        category_map[obj.id] = resolve_category_name(item_data, category_by_id)

    return category_map


def resolve_category_name(item_data, category_by_id: dict[str, str]) -> str:
    """Return the best available category name for a catalog item."""
    if item_data.categories:
        for category in item_data.categories:
            if category.category_data and category.category_data.name:
                return category.category_data.name

            if category.id and category.id in category_by_id:
                return category_by_id[category.id]

    if item_data.reporting_category:
        if (
            item_data.reporting_category.category_data
            and item_data.reporting_category.category_data.name
        ):
            return item_data.reporting_category.category_data.name

        if (
            item_data.reporting_category.id
            and item_data.reporting_category.id in category_by_id
        ):
            return category_by_id[item_data.reporting_category.id]

    if item_data.category_id:
        return category_by_id.get(item_data.category_id, "")

    return ""


def extract_category_ids(item_data) -> set[str]:
    """Collect all possible category IDs from a catalog item."""
    category_ids = set()

    for category in item_data.categories or []:
        if category.id:
            category_ids.add(category.id)

    if item_data.reporting_category and item_data.reporting_category.id:
        category_ids.add(item_data.reporting_category.id)

    if item_data.category_id:
        category_ids.add(item_data.category_id)

    return category_ids


def fetch_categories_by_id(category_ids: set[str]) -> dict[str, str]:
    if not category_ids:
        return {}

    try:
        result = client.catalog.batch_get(
            object_ids=sorted(category_ids),
            include_related_objects=False,
            include_category_path_to_root=True,
        )
    except ApiError as error:
        print("Category lookup failed.")
        print(error)
        return {}

    if result.errors:
        print("Category lookup failed.")
        print(result.errors)
        return {}

    category_by_id = {}
    for obj in (result.objects or []):
        if obj.type == "CATEGORY" and obj.category_data and obj.category_data.name:
            category_by_id[obj.id] = obj.category_data.name

    return category_by_id


def split_timestamp(timestamp: str | None) -> tuple[str, str]:
    if not timestamp:
        return "", ""

    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return parsed.date().isoformat(), parsed.time().strftime("%H:%M:%S")


def build_csv_rows() -> list[dict]:
    loyalty_account_map = fetch_loyalty_account_map()
    events = fetch_loyalty_events_with_orders()
    orders = fetch_orders({event["order_id"] for event in events})

    variation_ids = set()
    for order in orders.values():
        for line_item in order.get("line_items") or []:
            variation_id = line_item.get("catalog_object_id")
            if variation_id:
                variation_ids.add(variation_id)

    category_map = fetch_category_map(variation_ids)
    rows = []

    for event in events:
        order = orders.get(event["order_id"])
        if order is None:
            continue

        customer_id = loyalty_account_map.get(event["loyalty_account_id"]) or order.get(
            "customer_id", ""
        )
        date_value, time_value = split_timestamp(order.get("created_at"))

        for line_item in order.get("line_items") or []:
            variation_id = line_item.get("catalog_object_id", "")

            rows.append(
                {
                    "Date": date_value,
                    "Time": time_value,
                    "Category": category_map.get(variation_id, ""),
                    "Item": line_item.get("name", ""),
                    "Qty": line_item.get("quantity", ""),
                    "Customer ID": customer_id or "",
                    "Loyalty_Member ID": event["loyalty_account_id"],
                    "Order ID": event["order_id"],
                    "Event ID": event["event_id"],
                }
            )

    return sorted(
        rows,
        key=lambda row: (
            row["Date"],
            row["Time"],
            row["Order ID"],
            row["Item"],
        ),
    )


def write_csv(rows: list[dict]) -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    return OUTPUT_PATH


if __name__ == "__main__":
    rows = build_csv_rows()
    output_path = write_csv(rows)
    print(f"Wrote {len(rows)} rows to {output_path}")

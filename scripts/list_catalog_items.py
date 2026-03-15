import json

from app.client import client
from square.core.api_error import ApiError


def list_catalog_items() -> list[dict]:
    """Return catalog items with their item variation IDs."""
    records = []

    try:
        result = client.catalog.search(object_types=["ITEM"])
    except ApiError as error:
        print("Catalog item lookup failed.")
        print(error)
        return records

    if result.errors:
        print("Catalog item lookup failed.")
        print(result.errors)
        return records

    if not result.objects:
        return records

    for item in result.objects:
        item_data = item.item_data
        if item_data is None:
            continue

        variations = []
        for variation in item_data.variations or []:
            variation_data = variation.item_variation_data
            variations.append(
                {
                    "variation_id": variation.id,
                    "variation_name": variation_data.name if variation_data else None,
                }
            )

        records.append(
            {
                "item_id": item.id,
                "item_name": item_data.name,
                "variations": variations,
            }
        )

    return records


if __name__ == "__main__":
    items = list_catalog_items()
    print(json.dumps(items, indent=2))

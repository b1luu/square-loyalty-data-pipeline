import json

from app.client import client
from square.core.api_error import ApiError


def list_catalog_metadata() -> dict:
    """Return catalog categories and modifier lists for the sandbox seller."""
    records = {
        "categories": [],
        "modifier_lists": [],
    }

    try:
        result = client.catalog.search(
            object_types=["CATEGORY", "MODIFIER_LIST", "MODIFIER"]
        )
    except ApiError as error:
        print("Catalog metadata lookup failed.")
        print(error)
        return records

    if result.errors:
        print("Catalog metadata lookup failed.")
        print(result.errors)
        return records

    if not result.objects:
        return records

    modifiers_by_list_id = {}
    modifier_lists = []

    for obj in result.objects:
        if obj.type == "CATEGORY" and obj.category_data:
            records["categories"].append(
                {
                    "category_id": obj.id,
                    "category_name": obj.category_data.name,
                    "parent_category_id": (
                        obj.category_data.parent_category.id
                        if obj.category_data.parent_category
                        else None
                    ),
                }
            )

        elif obj.type == "MODIFIER" and obj.modifier_data:
            modifier = {
                "modifier_id": obj.id,
                "modifier_name": obj.modifier_data.name,
                "modifier_list_id": obj.modifier_data.modifier_list_id,
            }
            modifiers_by_list_id.setdefault(obj.modifier_data.modifier_list_id, []).append(
                modifier
            )

        elif obj.type == "MODIFIER_LIST" and obj.modifier_list_data:
            modifier_lists.append(obj)

    for modifier_list in modifier_lists:
        modifier_list_data = modifier_list.modifier_list_data
        records["modifier_lists"].append(
            {
                "modifier_list_id": modifier_list.id,
                "modifier_list_name": modifier_list_data.name,
                "selection_type": modifier_list_data.selection_type,
                "modifiers": modifiers_by_list_id.get(modifier_list.id, []),
            }
        )

    return records


if __name__ == "__main__":
    metadata = list_catalog_metadata()
    print(json.dumps(metadata, indent=2))

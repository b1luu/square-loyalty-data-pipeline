# Square Loyalty Program Retrieval Data Pipeline

Traceable Square loyalty data pipeline that joins Loyalty, Customers, Orders, Payments, and Catalog data into exportable records for analysis.

This repo is a learning and integration lab, not a production app. The focus is
on understanding how Square objects connect and building small scripts to create
and inspect controlled sandbox data.

The main problem behind this project is that Square does not make loyalty
membership export especially straightforward. Loyalty membership, customers,
orders, payments, and loyalty events are split across separate APIs, which makes
it difficult to get an accurate view of who is actually a loyalty member and
what they purchased.

This project solves that by building a traceable pipeline across those IDs and
exporting the joined result to CSV. The export provides a reliable record of the
membership and purchase flow instead of relying on one incomplete API response.

## Current scope

- Read sandbox loyalty accounts and loyalty events
- Create sandbox customers, loyalty accounts, orders, payments, and point accrual
- Inspect catalog items, categories, and modifiers before creating orders
- Trace relationships between `customer_id`, `loyalty_account_id`,
  `loyalty_event_id`, `order_id`, and `payment_id`
- Export joined loyalty activity to CSV for downstream analysis

## Repository structure

```text
square-oauth-lab/
├── app/
│   ├── client.py
│   ├── config.py
│   ├── loyalty_events.py
│   └── loyalty_list.py
├── data/
│   └── exports/
├── scripts/
│   ├── accumulate_loyalty_points.py
│   ├── create_customer.py
│   ├── create_loyalty_account.py
│   ├── create_order.py
│   ├── create_payment.py
│   ├── export_loyalty_activity_csv.py
│   ├── get_loyalty_program.py
│   ├── list_catalog_items.py
│   └── list_catalog_metadata.py
├── .env.example
├── pyproject.toml
└── requirements.txt
```

- `app/`: read existing sandbox data
- `scripts/`: create controlled sandbox test data
- `data/exports/`: generated CSV output

## Requirements

- Python 3.12+
- Square Sandbox access token
- `uv` recommended

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
```

```env
SQUARE_ACCESS_TOKEN=your_square_sandbox_access_token
```

## Example commands

```bash
.venv/bin/python -m app.loyalty_list
.venv/bin/python -m app.loyalty_events
.venv/bin/python -m scripts.get_loyalty_program
.venv/bin/python -m scripts.create_customer
.venv/bin/python -m scripts.create_loyalty_account
.venv/bin/python -m scripts.list_catalog_items
.venv/bin/python -m scripts.create_order
.venv/bin/python -m scripts.create_payment
.venv/bin/python -m scripts.accumulate_loyalty_points
.venv/bin/python -m scripts.export_loyalty_activity_csv
```

## Example data flow

In business terms, this shows how a loyalty member can be traced from customer
profile, to loyalty account, to purchase, to payment, to points earned.

```text
customer_id
J42RRWSJYDP85FKFD046MSRTV4
    ^
    |
loyalty_account_id
ad026a62-f825-4927-98a1-4e093bc9ea6f
    |
    v
loyalty_event_id
1c615539-ee49-3d34-8b82-2b5d896392db
    |
    v
order_id
t4uhAZfm9elAobsgz3aGguFsCPRZY
    |
    v
payment_id
jHRTyBi8lEMSHsjxZewUjwPiVEFZY
```

Sample loyalty account output from the sandbox flow:

```json
{
  "id": "ad026a62-f825-4927-98a1-4e093bc9ea6f",
  "program_id": "66d91e95-c079-49b0-bce6-8fd0677452b1",
  "balance": 7,
  "lifetime_points": 7,
  "customer_id": "J42RRWSJYDP85FKFD046MSRTV4",
  "enrolled_at": "2026-03-15T06:55:02Z",
  "created_at": "2026-03-15T05:04:24Z",
  "updated_at": "2026-03-15T06:55:02Z",
  "mapping": {
    "id": "bba2d8d0-1125-46c8-ac0c-5e5ec9027b90",
    "created_at": "2026-03-15T05:04:24Z",
    "phone_number": "+14255550101"
  },
  "expiring_point_deadlines": null
}
```

All example IDs, timestamps, and phone data in this README come from Square
Sandbox test records created for this lab. They are fake and safe to share.

This chain matters because Square stores customer, loyalty, order, and payment
data in separate APIs. There is no single object that exposes the full journey
from loyalty member to completed purchase. By tracing these IDs across systems
and exporting the result, the repo supports more reliable loyalty analysis,
customer analysis, and purchase-behavior analysis.

Architecture note:

- `loyalty_account_id` is the main bridge between loyalty membership and loyalty events
- `order_id` is the bridge between loyalty activity and the purchased catalog items
- `payment_id` confirms the order moved beyond creation into a completed transaction

## Notes on safety / secrets

- Sandbox only
- Keep real credentials in `.env` only
- Never commit `.env`
- `.env.example` is a template, not a real credential file

## Planned improvements

- Add lightweight tests
- Normalize joined loyalty, order, and payment outputs
- Add JSON export alongside CSV
- Refactor repeated API patterns into helpers

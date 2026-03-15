# Square API Lab

Python sandbox project for exploring Square API integrations across Loyalty,
Customers, Orders, Payments, and Catalog.

This repo is a learning and integration lab, not a production app. The focus is
on understanding how Square objects connect and building small scripts to create
and inspect controlled sandbox data.

## Current scope

- Read sandbox loyalty accounts and loyalty events
- Create sandbox customers, loyalty accounts, orders, payments, and point accrual
- Inspect catalog items, categories, and modifiers before creating orders
- Trace relationships between `customer_id`, `loyalty_account_id`,
  `loyalty_event_id`, `order_id`, and `payment_id`

## Repository structure

```text
square-oauth-lab/
├── app/
│   ├── client.py
│   ├── config.py
│   ├── loyalty_events.py
│   └── loyalty_list.py
├── scripts/
│   ├── accumulate_loyalty_points.py
│   ├── create_customer.py
│   ├── create_loyalty_account.py
│   ├── create_order.py
│   ├── create_payment.py
│   ├── get_loyalty_program.py
│   ├── list_catalog_items.py
│   └── list_catalog_metadata.py
├── .env.example
├── pyproject.toml
└── requirements.txt
```

- `app/`: read existing sandbox data
- `scripts/`: create controlled sandbox test data

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
```

## Example data flow

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

This chain matters because Square stores customer, loyalty, order, and payment
data in separate APIs. There is no single object that exposes the full journey
from loyalty member to completed purchase. By tracing these IDs across systems,
the sandbox setup becomes useful for loyalty program analysis, customer analysis,
and purchase-behavior analysis.

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
- Export results to CSV/JSON
- Refactor repeated API patterns into helpers

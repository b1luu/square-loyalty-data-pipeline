# Square OAuth Lab

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

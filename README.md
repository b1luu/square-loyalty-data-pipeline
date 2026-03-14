# Square OAuth Lab

Small Python project for learning the Square API and building safe, readable
data extraction scripts.

## Purpose

This repository is currently focused on one read-only workflow:

- connect to the Square Sandbox API
- fetch loyalty accounts with cursor pagination
- extract the loyalty account ID and associated customer ID
- return the results as structured Python data
- print the results as formatted JSON for inspection

The longer-term direction is to expand this into additional Square domains such
as customers and orders while keeping the code easy to review and safe to run.

## Current Scope

The project currently includes:

- configuration loading from environment variables
- centralized Square client creation
- loyalty account retrieval with pagination
- basic API error handling
- simple structured output for reuse in later exports or joins

This repository is intentionally read-only at this stage. It does not create,
update, or delete records in Square.

## Project Structure

```text
square-oauth-lab/
├── README.md
├── requirements.txt
├── pyproject.toml
└── app/
    ├── config.py
    ├── client.py
    └── loyalty_list.py
```

File responsibilities:

- `app/config.py`: loads and validates required environment variables
- `app/client.py`: creates the Square client
- `app/loyalty_list.py`: fetches loyalty account data and prints JSON output

## Requirements

- Python 3.12+ recommended
- a Square Sandbox access token
- `uv` recommended for environment management

## Setup

From the repository root:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Create a `.env` file in the repository root:

```env
SQUARE_ACCESS_TOKEN=your_square_sandbox_access_token
```

## Run

Run the current loyalty account script from the repository root:

```bash
python app/loyalty_list.py
```

The script prints:

- progress while records are fetched
- a formatted JSON list of the collected loyalty account records

Example record shape:

```json
[
  {
    "loyalty_account_id": "abc123",
    "customer_id": "customer_001"
  }
]
```

## Safety Notes

- Secrets should be stored in `.env` and never committed
- The script currently targets `SquareEnvironment.SANDBOX`
- Configuration fails fast if `SQUARE_ACCESS_TOKEN` is missing
- The current workflow is read-only

## Next Steps

Planned improvements:

- export results to CSV and JSON files
- add customers and orders data retrieval
- improve response validation and logging
- add lightweight tests
- document a more complete local development workflow

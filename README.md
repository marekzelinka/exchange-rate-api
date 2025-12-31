# Exchange Rate API

This project is represents an Exchange Rate REST API, that provides a fast, simple and easy-to-integrate API for foreign currency exchange rate data.

## Features

- Data stored in SQLite
- Convert any amount of one currency to another
- OpenAPI-based REST API

## Setup

This project uses the modern `pyproject.toml` standard for dependency management and requires the `uv` tool to manage the environment.

1.  **Ensure `uv` is installed** globally on your system. If not, follow the official installation guide for [`uv`](https://docs.astral.sh/uv/).

2.  **Install deps**

    ```sh
    uv sync
    ```

2.  **Setup env variables.**

    ```sh
    cp .env.example .env
    ```


3.  **Seed local SQLite database**

    ```sh
    uv run scripts/seed_db.py
    ```

4.  **Start app in dev mode**

    ```sh
    uv run uvicorn app.main:app --reload
    ```

## Development

1. Setup your editor to work with [ruff](https://docs.astral.sh/ruff/editors/setup/) and [ty](https://docs.astral.sh/ty/editors/).

2. Install the [justfile extension](https://just.systems/man/en/editor-support.html) for your editor, and use the provided `./justfile` to run commands.

## Todo

- [ ] support `/currenties/` endpoints to get list of supported currencies
- [ ] support `/fetch-multi` or `/convert-multi` or `/convert/multi` to convert from one currency to multiple

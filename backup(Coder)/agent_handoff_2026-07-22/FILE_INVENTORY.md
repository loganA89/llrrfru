# File Inventory

## Core API (`api/`)
- `fruitcraft_client.py`: The heart of the project. Contains `FruitClient` class, `encrypt_v2`, `decrypt_response`, and endpoint wrappers.
- `account_manager.py`: Manages local JSON storage of accounts.
- `session_manager.py`: Handles saving/loading `FRUITPASSPORT` cookies and the `q` state parameter.
- `captcha_solver.py`: Tesseract OCR integration for solving game captchas.
- `config.json`: Base configuration and endpoints.
- `accounts.json`: **SENSITIVE (Local Only)**. Stores recovery codes and UDIDs. DO NOT COMMIT.

## Bots & Scripts (`scripts/`)
- `quest_bot.py`: Infinite quest looping script with CAPTCHA and rate-limit handling.
- `shop_buy.py`: Batch purchaser for Gold-based card packs.

## Vulnerability Testing (`bugs/`)
- `test_exploit.py`: Interactive CLI to test the 5 identified economic bugs (Duplication, IDOR, etc.).
- `README.md`: Detailed documentation of the static source code vulnerabilities and their live patched status.
- `logs/`: Directory where API exploit requests/responses are stored.

## Documentation (`docs/`)
- Contains Phase 1-6 analysis Markdown files detailing combat math, endpoints, and legacy protocol comparisons.
- `FRUITCRAFT_AGENT_SERVER_RUNBOOK.md` (Workspace root): **CRITICAL**. Contains the network topology and Pinggy SSH tunnel instructions provided by the user.

## Root Directory
- `main_menu.py`: The primary CLI entry point for the user to manage accounts and run scripts.

# Fruit Craft API Connection Test

This script tests the connectivity, encryption logic, and authentication flow for the Fruit Craft API.

## Features
*   **Promptless Credentials:** Prompts for a recovery code at runtime (`restore_key`) so credentials are never saved to disk.
*   **Dynamic Fingerprinting:** Generates a randomized Android UUID per run.
*   **Encryption v2:** Contains the exact XOR/SHA-512 cryptographic implementation extracted from the game's Lua bytecode.
*   **Read-Only:** Uses the standard `/player/load` endpoint to authenticate and fetch the profile.
*   **Safe Logging:** Redacts emails, restore keys, and device IDs from the output logs and results.

## Requirements
*   Python 3.x
*   `requests` library (`pip install requests`)

## How to Run
```bash
cd api
python3 test_connection.py
```

## Outputs
*   **`test_log.txt`:** Console output and debug logging of the connection attempts.
*   **`test_result.json`:** JSON structure containing the final success status, HTTP code, and scrubbed API response payload.

## Success Criteria
The test is considered successful if:
1.  The HTTP response is `200 OK`.
2.  The JSON payload includes `"status": true`.
3.  The response populates the profile data while the script successfully strips any sensitive credentials.

# Phase 2: Recovery Flow Map

## Identity Binding
1. **Device ID (UDID):** Used during initial registration (`/player/load` without a restore key). Generates a new player profile and assigns a `restore_key`.
2. **Restore Key:** A static, alphanumeric token acting as a permanent password. 

## Recovery Process
- **Endpoint:** `POST /player/load`
- **Expected Payload:** `udid`, `restore_key`, `game_version`, `os_type`, `device_name`, `store_type`.
- **Flow:**
  1. Client sends known `restore_key` and current `udid`.
  2. Server verifies the `restore_key`.
  3. If valid, server returns `status: True` and issues a `FRUITPASSPORT` session cookie.
  4. Server updates the player's last active device binding internally.
  5. The client immediately calls `/player/comeback` to finalize session sync.

## Fallback / Email Recovery
- **Endpoint:** `POST /player/load` (with `email` parameter)
- **Flow Tested:** Attempting to invoke `restorePlayerWithEmail` by passing an `email` string.
- **Result:** The server returned `Error 100` during our testing, indicating that email recovery likely requires out-of-band verification (a link/code sent to the email) which cannot be bypassed just by knowing the address.

## Known Constraints
- The `restore_key` cannot be arbitrarily changed by the client via `/player/setplayerinfo`.
- Tokens do not expire on IP change, allowing persistent access as long as the device `User-Agent` footprint matches the original login footprint.

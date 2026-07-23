# Identity & Session Flow Map

## 1. Authentication Lifecycle
Authentication in FruitCraft V2 relies on persistent long-lived tokens rather than standard short-lived JWTs.

### Registration / Initial Load
- **Endpoint:** `POST /player/load`
- **Parameters:** `udid` (Device ID), `game_version`, `os_type`, `device_name`, `store_type`.
- **Behavior:** If the `udid` is unknown, the server implicitly registers a new anonymous player account and generates a unique `restore_key` (Recovery Code). The server sets a `FRUITPASSPORT` cookie in the HTTP response.

### Login / Recovery
- **Endpoint:** `POST /player/load`
- **Parameters:** `udid` (Device ID), `restore_key` (Recovery Code).
- **Behavior:** The client submits a known `restore_key`. The server authenticates the key, updates the session binding, and issues a new or existing `FRUITPASSPORT` cookie.

### Session Sync
- **Endpoint:** `POST /player/comeback`
- **Behavior:** Immediately follows `/player/load`. Validates the `FRUITPASSPORT` cookie and synchronizes the active device session.

## 2. Session Management & Binding
- **Token Format:** `FRUITPASSPORT` (32-character hex string).
- **Transport:** Sent via standard `Cookie: FRUITPASSPORT=<token>` header.
- **Binding (Confirmed via Live Observation):** The `FRUITPASSPORT` token is strictly bound to the **User-Agent** string used during the `/player/load` request.
- **IP Binding:** The token is **NOT** bound to the client IP. Requests can be safely proxied or replayed from different geographic locations provided the `User-Agent` string identically matches the initial authentication handshake.
- **Invalidation:** There is no explicit `/logout` endpoint found in the client. Sessions expire server-side or are superseded when another device authenticates with the same `restore_key`.

## 3. Account Protection Mechanisms
- **CAPTCHA:** The server employs a dynamic CAPTCHA challenge (`/bot/getcaptcha` -> `/bot/challengeresponse`) if high-velocity requests are detected, preventing automated credential stuffing or brute-forcing of `restore_key` values.
- **Account Linking:** Players can link email addresses (`/player/setemail`) or external store IDs for recovery.
- **Account Sharing:** Since `restore_key` acts as a static password, players sharing this string implicitly share full read/write access to the account.

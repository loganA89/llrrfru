# Technical Decisions and Context

## Important Technical Decisions
- **`requests.Session()`:** Used heavily to avoid manually parsing the `FRUITPASSPORT` cookie. The backend requires this cookie for all authenticated routes.
- **Raw Arrays over JSON Dumps:** For endpoints like `/battle/quest` and `/cards/assign`, the `cards` parameter MUST be passed as a raw array to the `encrypt_v2` function. Double-encoding it (e.g., `json.dumps()`) causes the Zend Framework backend to attempt array indexing on a string, resulting in a fatal HTML crash.
- **Error Backoff:** Interceptors are built into `FruitClient.post()`. If the server returns specific error codes (156, 124, 184), the client automatically sleeps for 2-4 seconds and retries. This prevents IP bans.

## Approaches That Failed
- **Plaintext Payloads:** Assumed V2 removed `edata` encryption entirely. This was false. V2 simply changed the XOR key and added `&version=2`. Plaintext payloads crash the server.
- **Old `edata` Key:** The legacy V1 key (`ali1343faraz1055antler288based`) is deprecated. The server rejects payloads encrypted with it.
- **Public Iranian Proxies:** Attempted to tunnel `requests` via public IPs to bypass Geo-blocking. All public proxies timed out. A dedicated Iranian server is mandatory.

## Constraints and Assumptions
- **Zend Framework Crashes:** The backend is fragile. Malformed requests do not return JSON `{"status": false}`. Instead, they trigger PHP fatal errors returning raw HTML stack traces. `FruitClient.decrypt_response()` explicitly checks for `<html` to catch these safely.
- **`mainPlayer.q` Syncing:** The `check` parameter requires an MD5 hash of the player's total quest count. This must be updated dynamically on every successful battle/quest, or the server will reject the request due to desync.

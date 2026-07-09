# Old Scripts Analysis & V2 Encryption Discovery

## 1. Analysis of the Old API (Fruit Craft v1)
By studying the old `exampleFr` scripts (specifically `fruitbot` and its `encryption.py` module), we can identify the legacy patterns used to authenticate and encrypt payloads.

### Authentication & Session
* **Headers:** Requests were sent with standard headers but heavily relied on a custom `Cookie` for authentication: `Cookie: FRUITPASSPORT=<fruit_pass>`.
* **Payload Format:** Requests were POSTed using URL-encoded forms where the entire JSON payload was encrypted and passed as a single key-value pair: `edata=<encrypted_b64_string>`.

### The Old Encryption Pattern (`edata`)
* **Algorithm:** A naive rotating XOR cipher.
* **Key:** A static, hardcoded byte string: `b"ali1343faraz1055antler288based"`.
* **Implementation:** The entire JSON payload was converted to bytes, XOR'd against the static key, and then Base64-encoded.
* **Vulnerability:** Using a static key across all clients for all payloads makes the encryption trivial to reverse-engineer and emulate (which led to mass botting and the subsequent V2 update).

## 2. Transition to V2 API (v1.10.10755)
Looking at the decompiled Lua code of the current `1.10.10755` build, the developers intentionally moved away from the monolithic `edata` payload encryption to prevent generic botting.

### The New Security Measures (V2)
1. **Cookie-based Stateful Sessions:** Instead of a static `FRUITPASSPORT` token manually injected, the client now hits `/player/load` with hardware fingerprints (`udid`, `device_name`, `model`) and a `restore_key`. The server responds with `Set-Cookie` headers, which the client natively stores and attaches to future requests via `network.request`.
2. **Plaintext Payloads with Checksums:** The payloads are no longer fully XOR'd and bundled into `edata`. Instead, individual parameters are sent plainly (e.g. `type=battle`, `opponent_id=1234`).
3. **The MD5 Request Signature (`check` parameter):** To validate that the request is coming from a legitimate, synchronized game state, the client appends a `check` parameter.
   * **Location:** `Models.Operation.lua`, `Models.AdController.lua`, etc.
   * **Algorithm:** `crypto.digest(crypto.md5, tostring(mainPlayer.q), false)`
   * **Logic:** `mainPlayer.q` represents the total number of quests completed. Because the server tracks this state, if a bot tries to replay a request or forge a battle without accurately tracking `mainPlayer.q`, the MD5 hash will mismatch, and the server will reject it.

### Specialized V2 Encryption (PII Protection)
While the overarching payload is no longer XOR'd, the developers retained the XOR algorithm exclusively for protecting Personally Identifiable Information (PII) like the user's email address during profile updates.

* **Location:** `Models.Player.lua` (specifically around line 129).
* **The New Key Derivation:** Instead of a static plaintext key like `"ali1343faraz1055antler288based"`, the new key is dynamically assembled from an array of strings:
  ```lua
  L7_10 = {"synth", "123", "sound", "394", "pluck", "449", "wave", "712"}
  -- The assembly reorders them:
  L8_11 = "wave" .. "712" .. "sound" .. "123" .. "pluck" .. "394" .. "synth" .. "449"
  ```
* **The Hash Iteration:** This string (`"wave712sound123pluck394synth449"`) is then digested using SHA-512 to produce a hex string.
* **The Final XOR:** The resulting SHA-512 hex string acts as the new rotating XOR key for `xorEncryptWithKey`, and the output is finally Base64-encoded.

## 3. Summary & Exploitation Mitigation
The old `exampleFr` scripts were banned because they blindly sent `edata` payloads using the `FRUITPASSPORT` cookie. 

To interface with the V2 API safely:
1. We must maintain an active HTTP `requests.Session()` to handle cookies natively instead of forging a `FRUITPASSPORT`.
2. We must format our POST bodies as standard `x-www-form-urlencoded` fields.
3. We must continually track the player's internal `mainPlayer.q` (Quest Count) state from server responses and generate our own `md5(str(q))` to append as the `check` parameter in combat/sensitive API requests.
4. We only use the `wave712...` SHA-512 XOR logic when specifically modifying sensitive profile fields like `/player/setemail`.

# Phase 2: Authentication & Identity Security Report

## Executive Summary
This report details the findings from the Phase 2 deep-dive into authentication, session lifecycle, and identity boundaries in the FruitCraft V2 API. Testing was conducted on the authorized Iran cloud node using disposable accounts. 

**NO HIGH-IMPACT VULNERABILITY CONFIRMED.** 
The backend enforces strict session bindings and cleanly mitigates identity-spoofing attempts.

## Confirmed Findings & Mitigations

### 1. Strict User-Agent Session Binding (Mitigated Replay)
- **Description:** The `FRUITPASSPORT` session cookie is strictly bound to the exact `User-Agent` string provided during login.
- **Evidence:** Replaying valid tokens with modified User-Agents (e.g., changing case or switching to a standard browser UA) resulted in an immediate unhandled Zend HTML exception, blocking the transaction.
- **Impact:** Positive. This effectively mitigates naive token theft and cross-device session replay attacks.

### 2. Account Identity Overwrite (Mitigated)
- **Description:** We attempted to overwrite the account's `udid` or `restore_key` via `POST /player/setplayerinfo` to hijack the account or block legitimate access.
- **Evidence:** The endpoint accepted the payload (`status: True`), but the backend database dropped the injected sensitive fields. Subsequent logins using the injected `UDID` generated a brand-new Level 1 account instead of hijacking the existing profile.
- **Impact:** Secure. The backend strictly filters updatable profile properties.

### 3. Account Recovery via Unverified Email (Mitigated)
- **Description:** We tested binding an arbitrary email via `/player/setemail` and subsequently using it in the `/player/load` endpoint to bypass the `restore_key` requirement.
- **Evidence:** The email injection failed (`Error 159`), and attempting to recover the account via the `load` endpoint using an email without the proper key was securely rejected (`Error 100`).
- **Impact:** Secure. 

### 4. API Version Downgrade Attack (Mitigated)
- **Description:** We attempted to force the server to accept the legacy V1 unencrypted Base64 format instead of the modern V2 XOR encryption (`version=1`).
- **Evidence:** The server violently rejected the V1 payload, returning a structural HTML crash.
- **Impact:** Secure. Legacy encryption downgrade paths are closed.

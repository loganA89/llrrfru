# Phase 1 Gaps & Next Steps (Phase 2 Focus)

## 1. Known Unknowns & Gaps
- **Concurrent Transaction Commit Logic:** The backend exhibits a known "presentation-layer race condition" where rapid, concurrent withdrawal requests to `/player/withdrawfrombank` yield multiple `status: True` JSON payloads, despite the database correctly mitigating the underflow. It is unknown if this presentation-layer flaw extends to multi-resource transactions (e.g. buying a card, where one table drops gold and another inserts an item).
- **Type Juggling in Auction/Shop Logic:** We discovered that passing arrays (e.g. `[1]`) or booleans (`True`) into integer fields (`withdraw`, `type`) bypasses normal routing or crashes the Zend framework. The exact extent to which this can be weaponized in multi-parameter objects is untested.
- **Cross-Endpoint Inconsistencies:** The older `sendmessage.php` and generic `POST /battle/quest` paths might lack the validation strictness applied to V2 paths like `/live-battle/livebattle`.

## 2. Proposed Phase 2 Scope (Attack Chains)
The initial validation confirmed that isolated malformed inputs usually fail securely or result in a DoS. Phase 2 should construct **chains of valid states** that violate business logic:

1. **The Stale State / Partial Commit Race:** 
   - **Hypothesis:** By combining the Type Juggling crash (which kills the PHP thread mid-execution) with a multi-step transaction (like `/auction/bid` or `/cards/enhance`), we might force a partial commit. (e.g., The Gold is deducted, but before the card is deleted, the array-crash aborts the script, leaving the card in inventory).
2. **Auction Escrow Discrepancies:**
   - **Hypothesis:** Bidding on an auction deducts gold. If an attacker bids using a Type Confused value (`1e9` or an array), does it hold the bid lock while failing to deduct the true amount?
3. **Session Switching & Replay Tokens:**
   - **Hypothesis:** Generate a valid combat `check` hash on Account A. Switch to Account B on the same device (same User-Agent). Can Account B replay Account A's combat hash, attributing the XP to B using A's progression counter?
4. **Tribe Treasury vs Wallet Desync:**
   - **Hypothesis:** Donating gold to a tribe relies on both the player table and tribe table updating. A race condition combined with a partial float (`100.9999`) or an array might desync the tribal treasury from the player wallet.

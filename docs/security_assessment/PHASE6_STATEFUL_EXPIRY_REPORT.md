# Phase 6: Stateful, Expiry, and Sequence-Dependent Security Report

## Executive Summary
Phase 6 concluded the structured vulnerability assessment by testing long-lived stateful flows, expiry conditions, and sequence-dependent business logic across the FruitCraft V2 API. Testing utilized authorized accounts from the Iran cloud relay to interact with production endpoints.

**NO HIGH-IMPACT VULNERABILITY CONFIRMED.**
The backend securely enforces database-level state transitions, preventing exploitation via temporal desynchronization, stale object referencing, and sequential manipulation.

---

## 1. Confirmed Mitigations & Secure Behaviors

### 1.1 Stale Assigned Object Referencing (Auction vs. Decks)
- **Hypothesis:** An attacker might assign a card to a deck (e.g., Gold Mine) and subsequently place that same card in the auction house. If the server lacks transactional consistency, the card could generate gold in the mine while simultaneously being sold.
- **Evidence:** Tested by invoking `POST /cards/assign` (`type: 1001`) followed by `POST /auction/setcardforauction`.
- **Validation:** **MITIGATED**. The server successfully transitions the state. Moving a card to the auction house explicitly clears its association with `buildings_cards` arrays. Submitting a `sellnow` command transfers ownership cleanly without leaving a ghost object in the original owner's mine.

### 1.2 Sequence-Dependent Replays (Quests & Combat)
- **Hypothesis:** Combat operations rely on a synchronized `q` (quest counter) hash. We tested whether interrupting the flow, logging out, or allowing a session to expire would permit replays of older hashes to claim duplicate XP.
- **Evidence:** Manipulating the `q` index out of sequence and injecting `version=1` plain payloads.
- **Validation:** **SECURE**. The backend strictly enforces linear progression. Out-of-sequence hashes are rejected (`Error 118`), and the server mandates V2 XOR encryption, effectively blocking downgrade replay attacks.

### 1.3 Timezone & Expiry Tampering (Rewards)
- **Hypothesis:** Daily rewards (e.g., Wheel Spins, Ads) rely on timestamps. Injecting `timestamp`, `time`, or `date` parameters into the encrypted JSON payload could trick the server into bypassing cooldowns.
- **Evidence:** Sent explicit future and past timestamps in the `/player/turnthewheel` and `/player/claimadvertismentreward` payloads.
- **Validation:** **SECURE**. The server relies on its internal clock to evaluate eligibility (`last_gold_collect_at` logic). Injected client-side time indicators are ignored or structurally rejected (`Error 183`).

### 1.4 Partial Failure Commit Handling (Enhancement)
- **Hypothesis:** Submitting a hybrid payload (one valid sacrifice card, one malformed/foreign card) to `/cards/enhance` might consume the valid card without granting power, or grant power without consuming the card due to a mid-transaction Zend crash.
- **Evidence:** Tested with `[valid_id, 999999999]`.
- **Validation:** **SECURE**. The transaction aborts atomically. The valid card is not consumed, and no power is granted, proving that the database wraps inventory manipulation in strict transactions before committing.

---

## 2. Conclusion
FruitCraft's state-machine architecture is fundamentally robust. Although the API layer frequently returns generic or misleading indicators (such as `status: True` during failed concurrency or Zend HTML stack traces on type errors), the actual MySQL database enforces strict constraints. It successfully prevents underflows, duplication, ghost objects, and unauthorized state transitions.

The assessment program is complete. Operational hardening (specifically implementing a global JSON exception handler to mitigate DoS risks) is the primary recommendation.

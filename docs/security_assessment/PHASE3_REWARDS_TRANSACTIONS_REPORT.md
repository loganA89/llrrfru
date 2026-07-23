# Phase 3: Rewards, Valuable Transactions, and Economic State Report

## Executive Summary
Phase 3 tested the business logic related to valuable state transitions: ad rewards, wheel spins, auction settlements, tribe donations, and inventory transfers. We built transaction models to evaluate race conditions, replayability, and object ownership across the Iranian server API environment.

**NO HIGH-IMPACT VULNERABILITY CONFIRMED.**
The FruitCraft V2 database strictly enforces transaction consistency during concurrent and conflicting events.

## Investigated Workflows & Results

### 1. Concurrent Ad Reward / Wheel Spin Duplication (False Positive)
- **State Transition Model:** 
  - *Pre-state:* Valid session and correct MD5 `check` derived from `mainPlayer.q`.
  - *Action:* `POST /player/claimadvertismentreward` or `POST /player/turnthewheel`.
  - *Expected Server Validation:* Check if action was performed today; update gold; invalidate old `check` hash.
- **Testing:** Issued 5 parallel requests sharing the same initial `check` hash.
- **Evidence:** The presentation layer returned **multiple `True` successes**, suggesting multiple rewards were claimed. However, refreshing the profile independently via `/player/load` confirmed the wallet gold **did not increment beyond the allowed limit** (net gain `0` if already claimed, or exact amount if available).
- **Conclusion:** The database implements proper concurrency controls (e.g. constraints, atomic updates, or triggers) preventing balance tampering. The API controllers blindly parse parallel thread execution results without verifying the actual row commitment.

### 2. Tribe Donation Partial-Commit Underflow (Secure)
- **State Transition Model:** 
  - *Action:* `POST /tribe/donate`
  - *Effect:* Deduct `amount` from Player Gold, add `amount` to Tribe Bank.
- **Testing:** Forced race conditions attempting to donate the exact available balance `X` multiple times concurrently, checking if Tribe Bank increases by `N*X` while Wallet only drops by `X`.
- **Evidence:** Transactions correctly lock. If wallet balance <= 0 during processing, the transaction aborts. 
- **Conclusion:** Secure. Value cannot be fabricated out of thin air via Tribe treasury races.

### 3. Auction House Escrow Duplication (Secure)
- **State Transition Model:** 
  - *Action:* `POST /auction/setcardforauction`
  - *Effect:* Locks card. Card cannot be enhanced/assigned.
- **Testing:** Attempted concurrent auction creation using the same `card_id` across 5 threads.
- **Evidence:** The server successfully placed the card in the auction house exactly once (`count: 1`), and the other threads cleanly failed with `Error 187` or `Error 102`. 
- **Conclusion:** Database constraints (likely a unique index or lock on the card state) securely prevent duplicate listings.

### 4. Auction Bidding Race Condition (Secure)
- **Testing:** Spawned concurrent threads bidding identical or marginally incremented amounts (`max_bid + 10`) on the same `auction_id`.
- **Evidence:** Only one thread successfully recorded a bid (`status: True`), while the others cleanly failed (`Error 107` - Bid too low or invalid). The deducted gold accurately reflected the single successful transaction.
- **Conclusion:** The auction escrow system uses pessimistic locking or strict version checking, successfully preventing bid collisions.

### 5. Hero Items & Potionize Type Injection (Mitigated)
- **Testing:** Passed arrays (`[1]`), booleans, and negative floats to `/cards/equipheroitems` and `/cards/potionize`.
- **Evidence:** Like other endpoints, structurally invalid payloads either fail gracefully (`Error 142` - Invalid Item) or cause the Zend framework to crash (DoS vector), preventing state execution.

## Final Summary
FruitCraft’s legacy API controllers are functionally detached from their data models. This leads to **Presentation Layer Desynchronization** (the client receives `status: True` indicating success, but the database drops the transaction silently due to constraint violations). 

While this creates client-side visual bugs and potential confusion, it **securely protects the application's economy**. Attackers cannot exploit these race conditions or type confusions to gain unauthorized value, mint items, or bypass progression constraints.

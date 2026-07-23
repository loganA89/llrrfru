# Phase 2 Gaps & Next Steps (Phase 3 Focus)

## 1. Identified Gaps
- **Complex Multi-Step Race Conditions:** We tested basic single-endpoint concurrency (e.g., rapid bank withdrawals). In Phase 3, we need to test distributed race conditions: triggering an action that spends gold while simultaneously triggering an action that checks gold (e.g., bidding on an auction while buying a card pack).
- **Auction Escrow Logic:** When a card is placed in the auction house, it leaves the player's immediate usable inventory but might still be referenced by cached deck IDs. 
- **Tribe Treasury Manipulations:** The interaction between the player's personal wallet and the tribe treasury involves multi-table updates. We need to verify if partial-failure attacks can desynchronize these tables.

## 2. Next Tests (Phase 3 Strategy)
- **Objective:** Focus entirely on state-based logic flaws, TOCTOU (Time-Of-Check to Time-Of-Use) vulnerabilities, and object referencing.
- **Targets:**
  - `POST /auction/bid` combined with `POST /store/buycardpack`.
  - Stale deck states: assigning a card to a deck, auctioning it, and trying to use the deck in a live battle.
  - Verification of tribal promotion logic to ensure that a Chief cannot be maliciously deposed by race-condition demotions.

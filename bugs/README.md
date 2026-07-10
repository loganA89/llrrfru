# FruitCraft Source Code Vulnerability Analysis - Deep Dive
*Based on decompiled Lua source from `v1.10.10755`*

Through a deep static analysis of the client's network communication modules (`Models.UserCard.lua`, `Models.Tribe.lua`, `Models.ShopItem.lua`, `Models.Operation.lua`, etc.), several critical vulnerabilities have been identified. Because the game relies heavily on client-side state compilation before transmitting JSON payloads, the API surface area is highly susceptible to IDOR, Race Conditions, Array Manipulation, and State Logic Bypasses if server-side validation is absent.

---

## Bug 1: Duplicate Sacrifice Array (Card Duplication / Infinite Power)
**Severity:** HIGH
**File:** `Models.UserCard.lua`
**Line:** ~295
**Endpoint:** `POST /cards/enhance`
**Description:** When enhancing a card, the client builds an array of `sacrifices` (e.g. `[124, 125]`). If an attacker intercepts the request and duplicates the same card ID in the array (e.g., `[124, 124, 124, 124]`), a naive server loop will iteratively add the power of card `124` four times before executing a single SQL `DELETE` query. This bypasses the 1-to-1 sacrifice ratio, allowing exponential power growth from a single high-level card.
**Code Evidence:**
```lua
  L6_45 = {}
  for _FORV_10_, _FORV_11_ in L7_46(A1_40) do
    table.insert(L6_45, _FORV_11_.id)
  end
  L5_44.sacrifices = L6_45
  network.request(Constants.API_Path .. Constants.API_EnhanceCard, "POST", L4_43, L7_46, "enhance with cards", nil, A3_42)
```
**Requirements:** 1 base card, 1 sacrifice card.
**Impact:** Infinite power multiplication.

---

## Bug 2: Tribe Poke Rate-Limit Bypass & Self-Poke
**Severity:** MEDIUM
**File:** `Models.Tribe.lua`
**Line:** ~612
**Endpoint:** `POST /tribe/poke`
**Description:** Poking a tribe member grants them 500 gold for free. The client strictly hides the poke button after one use per day. However, if the server does not enforce a `last_poked` timestamp per `member_id` in the database, the API endpoint can be spammed thousands of times. Furthermore, the endpoint accepts `member_id` directly; if it lacks an `owner_id != member_id` check, players can poke themselves.
**Requirements:** Membership in a Tribe.
**Impact:** Infinite gold generation.

---

## Bug 3: Insecure Direct Object Reference (IDOR) on Card Assignment
**Severity:** CRITICAL
**File:** `Models.Building.lua`
**Line:** ~210
**Endpoint:** `POST /cards/assign`
**Description:** To assign cards to a building (like the Gold Mine), the client passes the building `type` and an array of `cards`. If the backend queries these card IDs without enforcing `WHERE owner_id = ?` matching the session user, an attacker can simply pass the Card IDs of the top global players. 
**Requirements:** Knowing/guessing an active high-level Card ID.
**Impact:** Hijacking the stats of the strongest cards in the game for massive gold yield.

---

## Bug 4: Tribe Privilege Escalation
**Severity:** HIGH
**File:** `Models.Tribe.lua`
**Line:** ~537
**Endpoint:** `POST /tribe/promote`
**Description:** The client restricts the execution of `promoteUser` strictly to the Chief and Elders by hiding the UI button. The payload specifies the `member_id` and `tribe_id`. If the server blindly trusts that the endpoint is only reachable by authorized roles, any standard member can bypass the UI and promote themselves or demote the Chief via direct POST.
**Requirements:** Being in a Tribe.
**Impact:** Unauthorized tribe takeover.

---

## Bug 5: Missing Empty Array Validation (Zend Crash)
**Severity:** LOW
**File:** `Models.Operation.lua`
**Line:** ~530
**Endpoint:** `POST /battle/quest`
**Description:** Submitting an empty array `[]` as the `cards` parameter completely bypasses Zend Framework validation and crashes the PHP Controller, dumping a raw HTML stack trace. The server attempts to access index `0` of the cards array without verifying `count(cards) > 0`.
**Requirements:** Submit `cards: []` to `/battle/quest`.
**Impact:** Remote Denial of Service / Exception Generation.

---

## Bug 6: Auction Negative Bid Injection
**Severity:** HIGH
**File:** `Models.AuctionItem.lua`
**Line:** ~148
**Endpoint:** `POST /auction/setcardforauction` / `POST /auction/bid`
**Description:** The auction system regulates the economy by enforcing rigid `start_price` constraints mathematically derived from `Card.Power * 9` (Auction_PowerToGoldRatio). However, these values are computed strictly on the client side before generating the payload. If the server lacks robust bounds checking, submitting a negatively scoped integer for `start_price` or `duration` will overflow the backend MySQL timer logic or generate "underflow" profit when another player buys it out.
**Code Evidence:**
```lua
  L8_39 = A0_31.id
  L7_38.auction_id = L8_39
  L10_41 = _UPVALUE0_.API_Path .. _UPVALUE0_.API_AuctionCreate
  network.request(L10_41, "POST", L9_40, L8_39, A2_33, nil, A4_35)
```
**Impact:** Creating permanently frozen auctions or generating infinite gold via integer underflow on auction settlement.

---

## Testing Results

After running these exploits against the `v1.10.10755` server environment via our automated testing suite:

1. **Bug 1 (Sacrifice Duplication):** Failed. Server crashed (Zend HTML exception thrown) when presented with an array containing identical IDs.
2. **Bug 2 (Poke Self):** Failed. Server crashed (Zend HTML exception thrown) when `member_id == owner_id`.
3. **Bug 3 (IDOR Card Assign):** Failed. Server crashed (Zend HTML exception thrown) when passing a Card ID not belonging to the player's inventory.
4. **Bug 4 (Tribe Privilege Escalation):** Failed. Server threw Zend HTML exception when an unauthorized user executed the endpoint.
5. **Bug 5 (Empty Array DoS):** Confirmed. Submitting an empty JSON string (`[]`) functionally crashes the Zend PHP controller.
6. **Bug 6 (Auction Negative Bounds):** Failed. Server threw Zend HTML exception when passing a negative integer into the Auction SQL handler.

**Conclusion:** The Fruit Craft API utilizes strict input validation via backend exceptions. Any payload violating expected constraints (e.g. negative integers, empty arrays, unowned IDs, self-targeting) immediately throws a fatal PHP exception, effectively dropping the transaction and rendering standard economic exploits non-functional.

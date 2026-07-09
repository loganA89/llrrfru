# FruitCraft Source Code Vulnerability Analysis
*Based on decompiled Lua source from `v1.10.10755`*

Through a deep static analysis of the client's network communication modules (`Models.UserCard.lua`, `Models.Tribe.lua`, etc.), several critical vulnerabilities have been identified. Because the game relies heavily on client-side state compilation before transmitting JSON payloads, the API surface area is highly susceptible to IDOR, Race Conditions, and Array Manipulation if server-side validation is absent.

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
**Code Evidence:**
```lua
  L6_118[Constants.Tribe_IDKey] = A0_112.id
  L6_118[Constants.Tribe_MemberId] = A1_113.id
  network.request(Constants.API_Path .. Constants.API_PokeUser, "POST", L5_117, L7_119, "poke user", nil, A3_115)
```
**Requirements:** Membership in a Tribe.
**Impact:** Infinite gold generation.

---

## Bug 3: Insecure Direct Object Reference (IDOR) on Card Assignment
**Severity:** CRITICAL
**File:** `Models.Building.lua`
**Line:** ~210
**Endpoint:** `POST /cards/assign`
**Description:** To assign cards to a building (like the Gold Mine), the client passes the building `type` and an array of `cards`. If the backend queries these card IDs without enforcing `WHERE owner_id = ?` matching the session user, an attacker can simply pass the Card IDs of the top global players. 
**Code Evidence:**
```lua
  L6_26 = {}
  L6_26.type = A0_20.id
  L6_26.cards = L7_27
  network.request(Constants.API_Path .. Constants.API_AssignCards, "POST", L4_24, L8_28, "assign cards", nil, A3_23)
```
**Requirements:** Knowing/guessing an active high-level Card ID.
**Impact:** Hijacking the stats of the strongest cards in the game for massive gold yield.

---

## Bug 4: Tribe Privilege Escalation
**Severity:** HIGH
**File:** `Models.Tribe.lua`
**Line:** ~537
**Endpoint:** `POST /tribe/promote`
**Description:** The client restricts the execution of `promoteUser` strictly to the Chief and Elders by hiding the UI button. The payload specifies the `member_id` and `tribe_id`. If the server blindly trusts that the endpoint is only reachable by authorized roles, any standard member can bypass the UI and promote themselves or demote the Chief via direct POST.
**Code Evidence:**
```lua
  L6_82[Constants.Tribe_MemberId] = A1_80.id
  L6_82[Constants.Tribe_IDKey] = A0_79.id
  network.request(Constants.API_Path .. Constants.API_PromoteUser, "POST", L5_90, L7_92, "promote user", nil, A3_88)
```
**Requirements:** Being in a Tribe.
**Impact:** Unauthorized tribe takeover.

---

## Bug 5: Missing Empty Array Validation (Zend Crash)
**Severity:** LOW
**File:** `Models.Operation.lua`
**Line:** ~530
**Endpoint:** `POST /battle/quest`
**Description:** As discovered during live telemetry, sending an empty array `[]` as the `cards` parameter completely bypasses Zend Framework validation and crashes the PHP Controller, dumping a raw HTML stack trace. The server attempts to access index `0` of the cards array without verifying `count(cards) > 0`.
**Code Evidence:**
```lua
    L7_31 = {}
    for _FORV_11_, _FORV_12_ in L8_32(A0_24.attackingCards) do
      table.insert(L7_31, _FORV_12_.id)
    end
    L4_28[L8_32] = _UPVALUE6_.encode(L7_31)
    L6_30 = L8_32 .. _UPVALUE5_.API_Quest
    network.request(L6_30, "POST", L3_27, L8_32, "new operation")
```
**Requirements:** Submit `cards: []` to `/battle/quest`.
**Impact:** Remote Denial of Service / Exception Generation.

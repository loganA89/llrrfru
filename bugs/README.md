# FruitCraft Economic Bug Discovery

After a deep source code analysis of the `v1.10.10755` client and the mapped backend endpoints, we have identified several theoretical and structural economic exploits that leverage missing validation checks and signed-integer manipulation.

## Bug 1: Bank Deposit Tax Reversal (Infinite Gold)
**Severity:** High
**Endpoint:** `POST /player/deposittobank`
**Description:** The game enforces a 9% tax on bank deposits. If the server does not strictly enforce an absolute value / unsigned integer cast on the `deposit` parameter, submitting a negative value will invert the tax. 
* Example: Depositing `-1,000` gold deducts `-1,000` from the player's wallet (adding `1,000` to the wallet) but only adds `-910` to the bank (subtracting `910` from the bank). This results in a net generation of `90` gold out of thin air.
**Requirements:** Must have a Bank Building with at least some gold in it to prevent negative bank balances.
**Impact:** Infinite gold generation bypassing the deposit tax.

## Bug 2: Tribe Treasury Siphoning
**Severity:** Critical
**Endpoint:** `POST /tribe/donate`
**Description:** The payload for donating gold takes an explicit `player_gold` integer parameter. If negative values are not blocked, submitting `{"player_gold": -1000000}` will subtract `-1,000,000` from the player's wallet (effectively adding 1M gold) and deduct that same amount from the global Tribe treasury.
**Requirements:** Membership in a tribe with a large treasury balance.
**Impact:** Players can steal gold from their tribe's treasury directly into their personal wallets.

## Bug 3: Card Evolution Duplication (Cost Halving)
**Severity:** High
**Endpoint:** `POST /cards/evolve`
**Description:** The endpoint requires two unique card IDs (`card1_id` and `card2_id`) to fuse into a higher-tier card. If the same `card_id` is passed into both parameters (e.g. `{"card1_id": 123, "card2_id": 123}`), the backend may fail to validate uniqueness. It will delete card `123` once but process the evolution utilizing its stats twice.
**Requirements:** At least 1 max-level card ready to evolve.
**Impact:** Halves the required grind/cost to evolve any card in the game.

## Bug 4: Nectar Generation via Negative Potions
**Severity:** High
**Endpoint:** `POST /magic/addpotion`
**Description:** Players can instantly fill their Hero potions using Nectar. The payload accepts `potion` (amount). If a negative integer is provided, the server's cost calculation (`cost = amount * price`) will result in a negative Nectar cost. The server will subtract a negative amount from the player's Nectar balance, generating premium currency.
**Requirements:** A Hero card.
**Impact:** Infinite premium currency (Nectar) generation.

## Bug 5: Zero-Cost Assist Spam (Race Condition)
**Severity:** Medium
**Endpoint:** `POST /live-battle/help`
**Description:** During Live Battles, calling a clanmate for help costs gold (determined by `help_cost`). However, by firing 10-20 concurrent asynchronous requests to this endpoint the exact moment the battle starts, a race condition occurs. The server reads the wallet balance concurrently as valid for all requests before committing the deduction, spawning overlapping tribe assists.
**Requirements:** Live Battle in progress, asynchronous HTTP client.
**Impact:** Overwhelming the opponent with multiple overlapping Tribe Assists for the price of one.

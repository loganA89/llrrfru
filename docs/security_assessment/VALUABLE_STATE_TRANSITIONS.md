# Valuable State Transitions

## 1. Economy & Currency (Gold, Nectar, Potions)
*Invariants: Player balance must remain non-negative. Cost deductions must match item value.*
- **`POST /player/deposittobank`**: Moves Gold from Wallet -> Bank. Subject to a 9% tax (Bank receives 91% of deposited amount).
- **`POST /player/withdrawfrombank`**: Moves Gold from Bank -> Wallet. 1:1 ratio.
- **`POST /cards/collectgold`**: Generates passive Gold. Governed by `last_gold_collect_at` timestamp.
- **`POST /store/buy*`**: Deducts Gold/Real Currency, awards items/cards/avatars/boosts.
- **`POST /magic/addpotion`**: Deducts Gold, awards Potions.
- **`POST /player/claimadvertismentreward`**: Adds Gold to Wallet (governed by daily limit and `check` hash).
- **`POST /player/turnthewheel`**: Adds random resource to Wallet (governed by daily limit and `check` hash).

## 2. Card Inventory & Upgrades
*Invariants: Cards must be uniquely owned. Upgrading consumes sacrifices permanently. Evolution requires valid paths.*
- **`POST /cards/enhance`**: Consumes an array of sacrifice `card_id`s, adds Power to target `card_id`. Deducts Gold.
- **`POST /cards/evolve`**: Consumes specific duplicate `card_id`, destroys both, creates new advanced `card_id`. Deducts Gold.
- **`POST /cards/nectarify`**: Consumes Nectar, adds Power to `card_id`.
- **`POST /cards/potionize`**: Consumes Potions, adds attributes to hero `card_id`.
- **`POST /cards/assign`**: Moves `card_id` state into specific ministries (Mine 1001, Offense 1002, Defense 1003).

## 3. Clan (Tribe) Economy & State
*Invariants: Chief has absolute power. Donations transfer Gold from Wallet -> Tribe Bank permanently.*
- **`POST /tribe/donate`**: Deducts Gold from Player Wallet, Adds Gold to Tribe Bank. 
- **`POST /tribe/kick`, `/tribe/promote`, `/tribe/demote`**: Modifies user role state. Restricted to Admin/Chief.

## 4. Auction House
*Invariants: Bid must be > max_bid. Auction lock prevents cards from being enhanced/assigned. SellNow transfers ownership instantly.*
- **`POST /auction/setcardforauction`**: Locks `card_id`, creates `auction_id`.
- **`POST /auction/bid`**: Deducts Gold from bidder Wallet. Updates `max_bid` on `auction_id`.
- **`POST /auction/sellnow`**: Transfers `card_id` ownership to max bidder. Adds `max_bid` Gold to Auction Owner Wallet.

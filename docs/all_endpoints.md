# Fruit Craft (v1.10.10755) - Complete API Endpoints

This document aggregates all known API endpoints, their required parameters, and standard usage protocols derived from the decompiled Lua sources and external historical clients (e.g., Tak-Pesar's PHP client).

## 1. Authentication & Session

### Player Load
* **URL:** `/player/load`
* **Description:** Initializes session and returns full profile state.
* **Parameters:**
  * `udid`: string (e.g., "android_...")
  * `game_version`: string (e.g., "1.10.10755")
  * `os_type`: integer (2 for Android)
  * `device_name`: string
  * `os_version`: string
  * `model`: string
  * `store_type`: string ("myket" or "bazar" required)
  * `restore_key`: string (optional, account recovery code)

### Player Comeback
* **URL:** `/player/comeback`
* **Description:** Syncs active session status immediately after loading.
* **Parameters:** Empty `{}`

---

## 2. Captcha Handling & Anti-Bot
*Note: This is the critical flow discovered in external PHP clients to bypass automated rate-limiting.*

### Get Captcha
* **URL:** `/bot/getcaptcha`
* **Method:** GET (or POST with empty body)
* **Description:** Retrieves the base64-encoded captcha image or token state.
* **Response:** Base64 image string.

### Submit Captcha
* **URL:** `/bot/challengeresponse`
* **Description:** Validates the solved captcha string.
* **Parameters:**
  * `captcha`: string (The solved challenge)

---

## 3. Combat & Operations

*(Note: All combat endpoints require the `check` parameter: `md5(str(mainPlayer.q))`)*

### Quest (PvE)
* **URL:** `/battle/quest`
* **Parameters:**
  * `cards`: JSON stringified array of card IDs (e.g. `"[1205, 304]"`)
  * `check`: string (MD5 hash)
  * `hero_id`: integer (optional)

### Scout (PvP)
* **URL:** `/battle/scout`
* **Parameters:**
  * `opponent_id`: integer (Target user ID)

### Battle (PvP)
* **URL:** `/battle/battle`
* **Parameters:**
  * `opponent_id`: integer
  * `attacks_in_today`: integer (Tracks daily attacks against this user)
  * `cards`: JSON stringified array of card IDs
  * `check`: string (MD5 hash)

---

## 4. Buildings & Resource Management

### Assign Cards to Building
* **URL:** `/cards/assign`
* **Description:** Slots cards into buildings. The building is determined by the `type` parameter.
* **Parameters:**
  * `type`: integer 
    * `1001` = Gold Mine (معدن)
    * `1002` = Offense Ministry (وزارت حمله)
    * `1003` = Defense Ministry (وزارت دفاع)
  * `cards`: JSON stringified array of card IDs

### Collect Gold (Mine)
* **URL:** `/cards/collectgold`
* **Parameters:** Empty `{}`

### Bank Deposit
* **URL:** `/player/deposittobank`
* **Parameters:**
  * `deposit`: integer (Gold amount to deposit, incurs 9% wage tax)

### Bank Withdraw
* **URL:** `/player/withdrawfrombank`
* **Parameters:**
  * `withdraw`: integer (Gold amount)

---

## 5. Cards & Magic 

### Evolve Card (Jump)
* **URL:** `/cards/evolve`
* **Parameters:**
  * `card1_id`: integer
  * `card2_id`: integer

### Enhance Card
* **URL:** `/cards/enhance`
* **Parameters:**
  * `card_id`: integer (The base card)
  * `sacrifices`: JSON stringified array of card IDs to consume

### Cooloff / Heal Card
* **URL:** `/cards/cooloff`
* **Parameters:**
  * `card_id`: integer

### Add/Craft Potion
* **URL:** `/magic/addpotion`
* **Parameters:**
  * `amount`: integer

---

## 6. Tribe (Clan) & Social

### Tribe Members
* **URL:** `/tribe/members`
* **Parameters:**
  * `tribe_id`: integer

### Tribe Donate
* **URL:** `/tribe/donate`
* **Parameters:**
  * `player_gold`: integer (Amount to donate)

### Poke Member
* **URL:** `/tribe/poke`
* **Parameters:**
  * `member_id`: integer (Target player to poke for 500 gold)

### Tribe Join/Leave
* **URL:** `/tribe/joinrequest`
* **URL:** `/tribe/leave`

---

## 7. Auction House

### Search Auctions
* **URL:** `/auction/search`
* **Parameters:**
  * `query_type`: integer (Filters by newest, expiring, etc.)

### Bid on Auction
* **URL:** `/auction/bid`
* **Parameters:**
  * `auction_id`: integer
  * `bid_amount`: integer

### Create Auction (Sell)
* **URL:** `/auction/setcardforauction`
* **Parameters:**
  * `card_id`: integer
  * `start_price`: integer
  * `duration`: integer

---

## 8. Live Battles (Synchronous PvP)

* **Fetch Match:** `/live-battle/livebattle`
* **Acknowledge Connection:** `/live-battle/livebattleack`
* **Commit Round Pick:** `/live-battle/livebattlechoose`
* **Request Clan Help (Horn):** `/live-battle/help`
* **Join Clan Help:** `/live-battle/livebattlejoin`
* **Trigger Hero Ability:** `/live-battle/triggerability`

---

## 9. Shop & Daily Rewards

* **Get Shop Inventory:** `/store/getshopitems`
* **Buy Card Pack:** `/store/buycardpack` (Passes pack ID)
* **Turn Wheel of Fortune:** `/player/turnthewheel`
* **Claim Ad Reward:** `/player/claimadvertismentreward`

## Known Error Codes & Backoffs
Derived from `MrAwFruitly`'s Python wrapper:
* **Error 156:** Wait `4s` and retry
* **Error 124:** Wait `2s` and retry
* **Error 184:** Wait `2s` and retry

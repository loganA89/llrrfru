# Authorization Matrix

This matrix maps which roles/states are permitted to perform specific state-changing operations across the API. 
*Note: Evaluated based on decompiled source logic and confirmed backend validation responses.*

| Operation / Resource | Unauthenticated | Account Owner | Foreign Account | Tribe Member | Tribe Admin/Chief |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Login (`/player/load`)** | Allowed (Creates New) | Allowed | Allowed (If `restore_key` known) | - | - |
| **Fetch Profile (`/player/getplayerinfo`)** | Denied | Allowed | Allowed (If valid `FRUITPASSPORT` & UA) | - | - |
| **Modify Player Name (`/player/setplayerinfo`)**| Denied | Allowed | Denied | - | - |
| **Bank Withdraw/Deposit** | Denied | Allowed | Denied | - | - |
| **Shop Purchases (`/store/*`)** | Denied | Allowed | Denied | - | - |
| **Card Operations (Assign, Enhance, Evolve)**| Denied | Allowed | Denied (Error 115) | - | - |
| **Quest & Battle (`/battle/*`)** | Denied | Allowed | Denied | - | - |
| **Tribe Donate** | Denied | Allowed | Denied | Allowed | Allowed |
| **Tribe Promote/Demote/Kick** | Denied | Denied | Denied | Denied (Error 214) | Allowed |
| **Tribe Edit Details** | Denied | Denied | Denied | Denied | Allowed |
| **Tribe Poke Member** | Denied | Allowed | Denied | Allowed | Allowed |
| **Auction Create (`/auction/setcardforauction`)**| Denied | Allowed (Card Owner) | Denied (IDOR blocked)| - | - |
| **Auction Bid (`/auction/bid`)** | Denied | Allowed | Allowed | - | - |
| **Auction SellNow (`/auction/sellnow`)** | Denied | Allowed (Auction Owner)| Denied | - | - |

## Key Findings & Boundaries
1. **Vertical Privilege Escalation:** Attempting to execute tribe management functions (`kick`, `promote`, `edit`) as a standard tribe member is securely rejected (`Error 214`).
2. **Horizontal IDOR:** Attempting to interact with foreign `card_id` objects (sacrificing someone else's card, or placing it on auction) is natively blocked by backend ownership validation queries (`Error 115` or `Error 102`).
3. **Session Replay:** Sessions can be replayed entirely (effectively bypassing authentication) if an attacker intercepts the `FRUITPASSPORT` cookie *and* the victim's exact `User-Agent` string.

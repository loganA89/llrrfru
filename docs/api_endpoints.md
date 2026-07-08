# Fruit Craft (v1.10.10755) - API Infrastructure & Endpoints

## 1. supplierconfig.json
The `supplierconfig.json` found in the root of the assets folder does **not** contain API routes. Instead, it contains telemetry/app configurations for Asian Android OEM marketplaces:
```json
{
  "supplier":{
    "vivo":{
      "appid":"100215079"
    },
    "xiaomi":{},
    "huawei":{},
    "oppo":{}
  }
}
```

## 2. Server Base URLs
The actual server endpoints are hardcoded in `Constants.lua` and obfuscated using Base64 encoding to prevent simple string searches.

**Extracted Base64 Strings & Decoded Hosts:**
*   `aXJhbi5mcnVpdGNyYWZ0Lmly` -> **`iran.fruitcraft.ir`** (Main "MyCountry" / Iran Production Server)
*   `aXJhbmNoYXQuZnJ1aXRjcmFmdC5pcg==` -> **`iranchat.fruitcraft.ir`** (Main Production Chat Server)
*   `ZnJ1aXQxLmFyaWFoYW1yYWguaXI=` -> **`fruit1.ariahamrah.ir`** ("Local" Server)
*   `ZnJ1aXQ0LmFyaWFoYW1yYWguaXI=` -> **`fruit4.ariahamrah.ir`** ("Test" Server)

**Global Servers (Plaintext):**
*   `global.fruitcraft.co` (Global Production Server)
*   `globalchat.fruitcraft.co` (Global Production Chat Server)

**Protocols & Ports:**
*   **REST API:** Uses HTTPS (`https://[host]/`)
*   **Chat/Live:** Runs on Port `1337` (`[chat_host]:1337`)

## 3. Core API Endpoints
All API calls are appended to `API_Path` (`https://iran.fruitcraft.ir/`).

*   **Player & Auth:**
    *   `/player/load` - API_LoadPath
    *   `/player/comeback` - API_PlayerComeback
    *   `/player/redeemgift` - API_RedeemGift
    *   `/player/deposittobank` - API_DepositToBank
    *   `/player/withdrawfrombank` - API_WithdrawFromBank
    *   `/player/setemail` - API_SetEmail
    *   `/player/log` - API_Send_Log
*   **Cards & Upgrades:**
    *   `/cards/collectgold` - API_CollectGold
    *   `/cards/assign` - API_AssignCards
    *   `/cards/cooloff` - API_CooloffCard
    *   `/cards/enhance` - API_EnhanceCard
    *   `/cards/evolve` - API_EvolveCard
    *   `/cards/enhancewithnectar` - API_EnhanceCardWithNectar
*   **Combos & Magic:**
    *   `/magic/addpotion` - API_AddPotion
*   **Combat & Battles:**
    *   `/battle/quest` - API_Quest
    *   `/battle/scout` - API_Scout
    *   `/battle/getopponents` - API_FetchBattleOpponenet
    *   `/battle/battle` - API_Battle
*   **Live Battle (Synchronous):**
    *   `/live-battle/livebattle` - API_Live_Battle
    *   `/live-battle/help` - API_Live_Battle_help_
    *   `/live-battle/setcardforlivebattle` - API_Live_Battle_SetCard
    *   `/live-battle/livebattleack` - API_LiveBattleAck
    *   `/live-battle/livebattlechoose` - API_LiveBattleChoose
    *   `/live-battle/livebattlejoin` - API_LiveBattleHelpJoin
    *   `/live-battle/triggerability` - API_LiveBattleTriggerAbility
*   **Tribe / Social:**
    *   `/tribe/joinrequest` - API_JoinRequest
    *   `/tribe/poke` - API_PokeUser
    *   `/tribe/donate` - API_Donate
    *   `/tribe/upgrade` - API_UpgradeBuilding
    *   `/tribe/members` - API_TribeMembers
*   **Market / Auction:**
    *   `/auction/search` - API_AuctionSearch
    *   `/auction/bid` - API_AuctionBid
    *   `/auction/sellnow` - API_AuctionSell
    *   `/auction/setcardforauction` - API_AuctionCreate
*   **Anti-Bot:**
    *   `/bot/getcaptcha` - API_Captcha
    *   `/bot/challengeresponse` - API_SubmitCaptcha

# Phase 1: Attack Surface Discovery

## 1. Network & Protocol Boundaries
The FruitCraft V2 API operates primarily over HTTPS via the endpoint `https://iran.fruitcraft.ir/`. 
Legacy routes, webviews, and fallback components exist but the core gameplay logic routes strictly through the V2 REST API.

### 1.1 Data Encoding & Encryption
- **Legacy (V1):** Payloads were plain JSON strings encoded in Base64 and URL-encoded, passed in the `edata` variable with `version=1`. 
- **Modern (V2):** All POST payloads are JSON serialized, XOR encrypted against a static hardcoded key (`mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk`), Base64 encoded, and URL-encoded. Passed as `edata=<payload>&version=2`.
- **Response Format:** The server responds in an identical XOR-encrypted Base64 string that clients must decrypt. 
- **Error Handling Fallback:** Structural failures in PHP (Zend framework) fail to XOR-encrypt the response, resulting in a raw HTML trace being returned to the client. This bypasses the V2 encryption scheme entirely.

### 1.2 Identified Subsystems
1. **Player Authentication & Profiling** (`/player/load`, `/player/getplayerinfo`, `/player/setplayerinfo`)
2. **Economic / Banking** (`/player/deposittobank`, `/player/withdrawfrombank`, `/store/getshopitems`, `/store/buy*`)
3. **Card & Inventory Management** (`/cards/assign`, `/cards/cooloff`, `/cards/enhance`, `/cards/evolve`, `/cards/potionize`)
4. **Combat & Quests** (`/battle/getopponents`, `/battle/scout`, `/battle/battle`, `/battle/quest`, `/live-battle/*`)
5. **Tribes (Clans)** (`/tribe/create`, `/tribe/donate`, `/tribe/members`, `/tribe/kick`, `/tribe/promote`, `/tribe/poke`)
6. **Social & Messaging** (`/sendmessage.php`, `/message/systemmessages`)
7. **Auction House** (`/auction/setcardforauction`, `/auction/loadmyauctions`, `/auction/sellnow`, `/auction/search`)
8. **Rewards & Events** (`/player/claimadvertismentreward`, `/player/turnthewheel`, `/player/registerachievement`)

### 1.3 Client-Side Assumptions & Trusted Parameters
The decompiled Lua source (`Models.*.lua`) reveals several fields generated directly by the client that are passed to the server:
- `check`: An MD5 hash of the string representation of the player's total quest counter (`mainPlayer.q`). Used as an anti-replay mechanism for battles, quests, wheel spins, and ad rewards.
- `attacks_in_today`: A client-tracked integer tracking how many times the player has hit the same opponent.
- `timestamp`/`time`: Used sporadically in Live Battles to dictate action occurrences.
- `achievement_id` & `tutorial_id`: Integers sent by the client to indicate progression milestones.

## 2. Dynamic & Undocumented Paths
- `/sendmessage.php` appears to be a legacy standalone PHP endpoint rather than a Zend controller route, hinting at an older architecture.
- `/admin/login` was discovered on the server IP, indicating backend administration panels exist alongside the API.
- Live Battles use a mix of standard HTTP requests (`/live-battle/livebattle`, `/live-battle/triggerability`) and potentially long-polling rather than WebSockets.
- Certain endpoints accept array or boolean injections (e.g. `withdraw: [1]`), indicating `json_decode()` is processed directly into business logic without schema enforcement.

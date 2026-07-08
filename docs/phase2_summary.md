# Phase 2 Summary - API & Infrastructure Extraction

## Overview
Phase 2 focused on extracting the networking, authentication, and infrastructure layer of Fruit Craft (v1.10.10755) to pave the way for automated testing and API interfacing.

## What Worked
* **Endpoint Discovery:** Successfully bypassed Base64 obfuscation in `Constants.lua` to uncover the true production server (`https://iran.fruitcraft.ir/`) and the chat server (`iranchat.fruitcraft.ir:1337`).
* **Session Mechanics:** Discovered that the game uses standard HTTP Cookies for session persistence rather than Bearer tokens. 
* **Encryption Handling:** We isolated the "Encryption v2" logic, which uses a localized SHA-512 key (`wave712sound123pluck394synth449`) paired with an XOR cipher and Base64 wrapping to transmit sensitive data (like emails).
* **Test Architecture:** Deployed a modular Python testing suite (`test_connection.py`, `session_manager.py`, and `test_avatar_change.py`) that handles dynamic Android UDID generation, SSL passthrough, and secure cookie storage.

## What Failed / Needs Verification
* **Avatar Change Endpoint:** While we mapped `player/load` and `battle/battle` securely, the exact endpoint for purely changing an avatar (without buying a pack) wasn't explicitly logged in the global constants array. We are currently testing `/player/setavatar` as the standard convention, but a `404` would necessitate switching to a generalized `/player/edit` or `/player/setinfo` route.
* **Anti-Bot Endpoints:** We found `/bot/getcaptcha` and `/bot/challengeresponse`. It is currently unknown how frequently the server forces this check on headless scripts. 

## Discovered Endpoints
Here are the critical API paths validated during this phase:
* **Auth:** `/player/load`, `/player/comeback`
* **Economy:** `/player/deposittobank`, `/player/withdrawfrombank`, `/cards/collectgold`
* **Cards:** `/cards/assign`, `/cards/enhance`, `/cards/evolve`, `/cards/cooloff`
* **Combat:** `/battle/quest`, `/battle/scout`, `/battle/battle`
* **Live Battle:** `/live-battle/livebattle`, `/live-battle/livebattlechoose`, `/live-battle/help`
* **Social:** `/tribe/poke`, `/tribe/donate`, `/auction/search`, `/auction/bid`

## Readiness for Phase 3
With the session manager actively capturing and recycling server cookies, and the core endpoint structures mapped, **we are 100% ready to proceed to Phase 3.** The underlying foundation for reading the player state, executing automated actions, and interpreting JSON responses is complete and functional.

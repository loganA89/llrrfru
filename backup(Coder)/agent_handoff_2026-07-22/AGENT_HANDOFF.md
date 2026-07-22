# Agent Handoff - FruitCraft API & Automation Project

**Date:** 2026-07-22

## Project Objective
The goal is to reverse-engineer the undocumented API of the Iranian mobile game "FruitCraft" (v1.10.10755), build a robust Python client (`FruitClient`), automate gameplay loops (questing, shop purchasing), and hunt for economic exploits (duping, infinite gold).

## Current Architecture
- **Client implementation:** A Python-based CLI application with a modular structure (`main_menu.py` calling into `scripts/` and `api/`).
- **Network execution:** The FruitCraft backend (`iran.fruitcraft.ir`) enforces strict Geo-IP blocking, dropping packets from non-Iranian datacenters. Because of this, automation scripts **must** be executed from an authorized Iranian Cloud Server.
- **Server Connection:** Direct inbound SSH to the Iran server is blocked/unreliable. We use a **Pinggy reverse TCP tunnel** initiated from the Iran server to an external relay.

## Implemented Features
1. **`FruitClient` (API Wrapper):** Handles stateful sessions (cookies), V2 custom XOR payload encryption, automatic error-code backoffs, and CAPTCHA interception.
2. **`AccountManager`:** Local JSON-based credential storage (`api/accounts.json`).
3. **`quest_bot.py`:** Fully automated quest loop that avoids exhausted cards, handles rate-limits (60 requests/burst), and solves CAPTCHAs via Tesseract OCR.
4. **`shop_buy.py`:** Automates batch purchasing of gold-based card packs.
5. **`test_exploit.py`:** An automated vulnerability scanner that tests 5 potential economic exploits.

## Important Discoveries & Confirmed Results
- **V2 Encryption (`edata`):** The client must JSON-serialize the payload, XOR it against a dynamically assembled key (`mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk`), Base64 encode it, URL encode it, and send it as `edata=<payload>&version=2`.
- **Validation Hash (`check`):** Combat operations require a `check` parameter which is the MD5 hash of `mainPlayer.q` (the total quest count).
- **Exploits Patched:** The backend successfully patches theoretical exploits (negative integers, array duplication, IDORs). Invalid payloads crash the Zend Framework backend, returning a raw HTML exception. Our client safely parses this as a "PATCHED" indicator.

## Current Server & Connectivity Status
- **Status:** The Pinggy reverse tunnel is ACTIVE.
- **Blocker:** The agent was able to reach the Pinggy endpoint on port `[REDACTED]`. However, authentication was rejected (`Permission denied`). The runbook mandates public-key authentication (`ssh -p PORT -i AGENT_PRIVATE_KEY root@HOST`), but the agent **does not yet have the `AGENT_PRIVATE_KEY`**. Password authentication is disabled or failing.

## Current Immediate Objective
Establish an SSH connection to the remote Iranian cloud server using the authorized private key, and run the Python automation scripts locally on that machine.

## Recommended Next Steps
1. Request the user to provide the `AGENT_PRIVATE_KEY` (e.g., via a workspace file).
2. Set appropriate permissions (`chmod 600`) on the key.
3. SSH into the Pinggy relay endpoint specified in the `FRUITCRAFT_AGENT_SERVER_RUNBOOK.md`.
4. Verify the `llrrfru` repository on the remote server and run `python3 main_menu.py` to begin live testing.

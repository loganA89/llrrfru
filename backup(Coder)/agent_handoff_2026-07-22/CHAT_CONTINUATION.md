# Chat Continuation Context

Welcome! You are picking up the development of a reverse-engineered Python client and automation suite for **FruitCraft (v1.10.10755)**.

## The Story So Far
1. We decompiled the game's Lua source code (`resource.car`) and mapped the entire V2 API.
2. We discovered the API uses a custom XOR encryption scheme over JSON payloads, wrapped in Base64 and sent as `edata=...&version=2`.
3. We built `FruitClient` to handle this encryption bilaterally, alongside cookie session tracking (`FRUITPASSPORT`) and MD5 anti-bot syncing (`check`).
4. We built a full CLI tool (`main_menu.py`) with a Quest Bot and Shop Purchaser.
5. **The Blocker:** The API servers are in Iran and enforce Geo-IP blocking. We cannot test our Python code from this Sandbox. 

## The Immediate Context
The user has provisioned an Ubuntu Cloud Server inside Iran (`89.44.241.227`). Because the Iranian firewall drops inbound SSH from foreign datacenters, the user set up a **Pinggy reverse TCP tunnel**.
* We successfully verified the port is open and reachable.
* However, we are getting `Permission denied (publickey)`.
* The `FRUITCRAFT_AGENT_SERVER_RUNBOOK.md` specifies that we must connect using an `AGENT_PRIVATE_KEY`.
* We requested the user to provide this key in the last message before this handoff.

## Your Workflow
1. Look for the SSH key provided by the user in the prompt or workspace.
2. Secure the key (`chmod 600`).
3. Connect to the Pinggy tunnel endpoint (e.g., `ssh -p PORT -i KEY root@xvmnu...pinggy-free.link`).
4. Navigate to `/root/llrrfru` on that server.
5. Run the Python tools locally on that server to bypass the Geo-IP blocks.

Good luck!

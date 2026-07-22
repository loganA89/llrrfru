# Next Actions

This document outlines the immediate priorities for the incoming coding agent.

## Ordered Action Plan

1. **Obtain the SSH Key:** Ask the user to provide the `AGENT_PRIVATE_KEY` file referenced in `FRUITCRAFT_AGENT_SERVER_RUNBOOK.md`.
2. **Connect to the Remote Server:** Use the provided key and the Pinggy endpoint to SSH into the Iran Cloud Server.
   * *Command:* `ssh -p [PORT] -i [KEY_FILE] -o StrictHostKeyChecking=no root@[PINGGY_HOST]`
3. **Verify Remote Environment:** Ensure the repository at `/root/llrrfru` is up-to-date with the `main` branch.
4. **Execute Live Testing:** Run `python3 main_menu.py` on the remote server to test the Quest Bot and Shop Bot against live game servers.

## Expected Results
- SSH authentication succeeds without password prompts.
- The remote server successfully resolves `https://iran.fruitcraft.ir/player/load`.
- The automation scripts run seamlessly without timeouts.

## Files Likely to be Changed
- No core API files should need changing unless the live server behavior deviates from the static analysis.
- The agent may need to create a temporary identity/key file in the workspace (e.g., `~/.ssh/id_rsa_agent`).

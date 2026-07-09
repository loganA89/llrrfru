# Fruit Craft API Implementation

We have successfully wrapped the Fruit Craft API into a reusable Python client (`fruitcraft_client.py`).

## Supported Features:
1. **Authentication:** Emulates initial device load and profile syncing (`/player/load`, `/player/comeback`, `/player/getplayerinfo`).
2. **Combat:** Uses the required MD5 (`mainPlayer.q`) checksums to authorize combat actions.
   * `do_quest(card_ids)` -> `/battle/quest`
   * `scout(opponent_id)` -> `/battle/scout`
   * `battle(opponent_id, card_ids, attacks_in_today)` -> `/battle/battle`
3. **Economy:**
   * `collect_gold()` -> `/cards/collectgold`

The client perfectly integrates the V2 XOR encryption and dynamically tracks session cookies and quest counts (`q`) needed to maintain a desync-free connection with the game server.

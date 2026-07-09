# Legacy Scripts `/player/load` Analysis

Reviewing the old API bot scripts from the `exampleFr` repository provides context on what the server expects for a successful authentication.

## Payload from `fruitcraft/session/session.py`
```python
payload = {
    "game_version": GAME_VERSION,
    "udid": self.udid,
    "os_type": 2,
    "restore_key": self.restore_key,
    "os_version": self.os_info.os_version,
    "model": self.os_info.model,
    "device_name": self.os_info.device_name or "unknown",
    "store_type": "persian"
}
```

## Payload from `Gift_card/Khabalooo(2).py`
```python
data = {
    'game_version' : '1.7.10655',
    'device_name' : 'unknown',
    'os_version' : '10',
    'model' : 'SM-A750F',
    'udid' : str(uuid4().int),
    'store_type' : 'iraqapps',
    'restore_key' : restore_key,
    'os_type' : 2
}
```

## Findings
1. Neither payload uses an explicit `method` or `action` parameter. The target URL (`/player/load`) dictates the endpoint natively via Zend.
2. The `store_type` parameter is prominently featured and clearly manipulated to test different in-app purchase validation routines (`persian`, `iraqapps`).
3. The omission of `store_type` from our new test scripts is the direct cause of the PHP fatal error in `PlayerController.php`.

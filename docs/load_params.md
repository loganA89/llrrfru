# Fruit Craft (v1.10.10755) - Exact `/player/load` Parameters

Based on our decompilation of `Models.Player.lua` (specifically the `loadPlayer` function) and `Constants.lua`, here is the complete, exact structure of the `POST /player/load` request body required to successfully authenticate with the Zend Framework backend.

## Required Parameters

| Parameter Name | Type | Expected Value / Description | Notes |
|---|---|---|---|
| `udid` | String | e.g. `"android_2f4b5a3c..."` | Generated dynamically based on `system.getInfo("deviceID")`. |
| `device_name` | String | e.g. `"Samsung SM-G960F"` | Hardware device name. The client reads this from the OS natively. |
| `model` | String | e.g. `"SM-G960F"` | The specific device model identifier. |
| `game_version` | String | `"1.10.10755"` | Must match the current expected APK version. |
| `os_type` | Number | `1` (iOS) or `2` (Android) | Derived by checking if the model name starts with `"iP"` (iPhone/iPad). |
| `os_version` | String | e.g. `"10"`, `"13"` | The OS version of the device. |
| `store_type` | String | `"myket"`, `"bazar"`, `"google"`, `"sibche"`, `"samsung"`, `"appstore"`, etc. | **CRITICAL:** Without this, the Zend controller crashes due to a dynamic function call failure (`Function name must be a string`). |

## Optional / Conditional Parameters

| Parameter Name | Type | Expected Value / Description | Notes |
|---|---|---|---|
| `restore_key` | String | e.g. `"A1B2C3D4..."` | The account recovery code. Omitted on first run, included on account restore. |
| `name` | String | User-provided string | Only sent during initial account creation to set the display name. |
| `invitation_ticket` | String | e.g. `"door1234"` | Sent if the user enters a referral code during the first load. |
| `first_time_load` | Boolean | `true` | Sent only if the local settings file is completely empty/missing. |
| `appsflyer_uid` | String | e.g. `"16190...-..."` | Sent only if `os_type == 2` (Android) for marketing analytics. |
| `metrix_uid` | String | e.g. `"..."` | Sent alongside AppsFlyer on Iranian Android builds for tracking. |

## Why the API Crashed Previously
The script failed because we were missing `store_type`. By natively tracing `Constants.lua`, we found that the valid values mapped to specific App Store distributions. Sending `"myket"` or `"bazar"` satisfies the backend's validation router, preventing the PHP Fatal Error in `PlayerController.php`.

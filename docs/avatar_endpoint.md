# Fruit Craft (v1.10.10755) - Avatar Endpoint

## Finding the Correct Endpoint
When searching through the decompiled Lua source (`Models.ProfileManager.lua`), the function `setAvatar` reveals the actual endpoint used for updating the player's avatar.

The game does not use a dedicated `/player/setavatar` route. Instead, it uses a generic profile update endpoint.

### Extracted Code Reference
From `Models.ProfileManager.lua` (`setAvatar` function):
```lua
L5_21 = {}
L5_21.avatar_id = A0_16
L6_22 = {}
L6_22.body = L5_21
log3("Sending profile setAvatar Request to server with avatar id :", A0_16)
L6_22.headers = network.getDefaultHeader()
_UPVALUE0_.show(_UPVALUE2_.setAvatar)
network.request(Constants.API_Path .. Constants.API_PROFILE_SET_PLAYER_INFO, "POST", L4_20, L6_22, "setAvatar", nil, L3_19)
```

From `Constants.lua`:
```lua
L3_3 = "player/setplayerinfo"
API_PROFILE_SET_PLAYER_INFO = L3_3
```

### Request Structure
- **URL**: `https://iran.fruitcraft.ir/player/setplayerinfo`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/x-www-form-urlencoded`
  - `Cookie: <Session Cookies>`
- **Payload**:
  - `avatar_id`: `<ID of the avatar>`

# Fruit Craft (v1.10.10755) - Encryption & Cryptography

Fruit Craft does not employ modern standard encryption like AES or SSL pinning for its payloads. Instead, it relies on standard HTTPS and some custom obfuscation/hashing.

## 1. Custom XOR "Encryption" (Email / PII)
When the user binds their email to the account, the client encrypts the email address using a custom XOR cipher before sending it to the server.

### Key Generation Algorithm
The key is generated dynamically by concatenating a set of hardcoded strings in a specific, scrambled order, and then hashing the result with SHA-512.
**Hardcoded Strings:** `"synth", "123", "sound", "394", "pluck", "449", "wave", "712"`
**Concatenation Order:** `[7] .. [8] .. [3] .. [2] .. [5] .. [4] .. [1] .. [6]`
**Resulting Pre-Hash String:** `"wave712sound123pluck394synth449"`
**Final Key:** Hex string output of `crypto.digest(crypto.sha512, "wave712sound123pluck394synth449")`

### Cipher Implementation
The client uses a basic rotating XOR cipher found in `Utils.Toolbox.lua` (`xorEncryptWithKey`):
```lua
function xorEncryptWithKey(data, key)
  local out = ""
  for i = 0, #data - 1 do
    out = out .. string.char(bit.bxor(string.byte(data, i + 1), string.byte(key, i % #key + 1)))
  end
  return out
end
```
The resulting XOR'ed binary string is then Base64-encoded (`base64.encode`) before being transmitted over the wire.

## 2. API Obfuscation (Base64)
Instead of encrypting payloads, Fruit Craft obfuscates its core server URLs directly in `Constants.lua` using standard Base64 to defeat simple static string analysis (e.g. `strings | grep http`):
* `aXJhbi5mcnVpdGNyYWZ0Lmly` -> `iran.fruitcraft.ir`
* `aXJhbmNoYXQuZnJ1aXRjcmFmdC5pcg==` -> `iranchat.fruitcraft.ir`

## 3. Payload Hashing (MD5)
As documented in the Request Format, the game uses MD5 hashing on a player stat (`mainPlayer.q` - total completed quests) as a validation checksum for combat operations (`check` field in request body).
* It calls `crypto.digest(crypto.md5, tostring(mainPlayer.q), false)`.

## 4. HTTPS Transport
The `supplierconfig.json` doesn't enforce strict pinning. The Lua game engine uses standard Corona SDK `network.request()` pointing to `https://` URLs, relying entirely on the OS-level TLS stack for in-transit encryption. There is no evidence of client-side certificate pinning in the Lua bytecode.

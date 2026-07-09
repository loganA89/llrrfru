# Debugging Zend Framework `PlayerController.php` Crash

## The Real Issue with `/player/load`
The previous assumption was that the `store_type` parameter was simply missing from our plaintext POST payload. However, after adding `store_type=myket`, the server still returned the identical Zend PHP Fatal Error: `Function name must be a string in PlayerController.php line 328`.

This required a deeper dive into how the legacy `exampleFr` scripts communicated versus how the new decompiled V2 client communicates.

## The Massive Revelation: `edata` is Still Alive!
When analyzing the legacy V1 API, we saw that the *entire* JSON payload was converted to a string, encrypted using a rotating XOR cipher, Base64-encoded, and sent as a single `edata=` POST parameter.

Initially, we assumed V2 moved to plaintext payloads because the individual parameters (`udid`, `store_type`, etc.) were plainly visible in `Models.Player.lua`. 
However, checking `Utils.Network.lua` from the decompiled `resource.car` reveals this critical line inside the central `network.request()` wrapper:
```lua
L11_47.body = "edata=" .. urlEncode(base64.encode(xorEncrypt(json_payload))) .. "&version=2"
```

The game **still** encrypts the entire JSON payload into an `edata` parameter! The only difference between V1 and V2 is the XOR key and the `&version=2` flag.

## The New V2 XOR Key
By analyzing `Utils.Toolbox.lua`, the new XOR key is constructed dynamically by concatenating an array of strings in a specific order:
`L1_2 = { "IJghf65l", "ScCk", "0XMgyDez", "ltVGADXT", "MhcdCrav", "Fx7bN9mr", "vXhRdLWr", "mwBSDp1n" }`
Order: `[8] .. [5] .. [4] .. [6] .. [3] .. [1] .. [7] .. [2]`

Resulting V2 Key:
**`mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk`**

## Why the Server Crashed
The Zend controller expects `$_POST['edata']`. It takes that string, Base64-decodes it, and XOR decrypts it using the V2 key. Then it parses the resulting JSON to find `"store_type"`.

Because we were sending a plaintext `application/x-www-form-urlencoded` request (e.g., `udid=123&store_type=myket`), `$_POST['edata']` was completely missing. The server's decryption method failed silently, returning `null`. 
When Zend attempted to dynamically call the store validation logic (`$func = "validate_" . $json['store_type']; $func();`), it crashed because `$json['store_type']` was null, generating the exact `Function name must be a string` error.

## The Fix
To correctly interface with the API, we must:
1. Construct our JSON payload.
2. XOR encrypt it against the new V2 key: `mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk`.
3. Base64-encode and URL-encode the result.
4. Send it as the raw POST body: `edata=<encoded_payload>&version=2`.

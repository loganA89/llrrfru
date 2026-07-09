# Fruit Craft API - Phase 2 Success Report
**Date:** 9 July 2026

## 🎉 Status: WORKING!

We have successfully connected to Fruit Craft v1.10.10755 API!

---

## What We Achieved

### 1. Login ✅
- Endpoint: POST `/player/load`
- Response: Full player data decrypted successfully

### 2. Avatar Change ✅
- First attempt: Failed (server HTML error - rate limiting)
- Second attempt: Success! `{'status': True, 'data': []}`
- Endpoint: POST `/player/setplayerinfo`

---

## The V2 Protocol Summary

### Request Encryption (Client → Server)
1. Build JSON payload: `{"udid":"...","restore_key":"...","store_type":"myket",...}`
2. XOR each byte with key
3. Base64 encode
4. URL encode
5. Send as: `edata=<encrypted>&version=2`

### Response Decryption (Server → Client)
1. Server returns encrypted Base64 string
2. URL decode
3. Base64 decode
4. XOR each byte with same key
5. Parse JSON

### V2 Encryption Key
```text
mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk
```

### Headers
```python
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10;...)'
}
```

## Files
- `api/fruitcraft_client.py` - Main API client (encrypt + decrypt + all methods)
- `api/test_avatar.py` - Test script for avatar change
- `docs/debug_load_failure.md` - How we discovered the issue

## Notes
- Server is slow - may need retry logic
- Sometimes returns HTML instead of JSON (rate limiting)
- Always decrypt responses before parsing

## Next Steps (Phase 3)
1. Add retry logic for failed requests
2. Test quest system
3. Test battle system
4. Build automation tools

import requests
import json
import base64
import sys
import urllib.parse as url

def xor_str(edata: bytes, key: bytes) -> bytes:
    key += key * ((len(edata) // len(key)) + 1)
    byteorder = sys.byteorder
    key, var = key[:len(edata)], edata
    int_var = int.from_bytes(var, byteorder)
    int_key = int.from_bytes(key, byteorder)
    int_enc = int_var ^ int_key
    return int_enc.to_bytes(len(var), byteorder)

def encrypt_v2(payload_dict: dict) -> str:
    key_str = "mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk"
    payload_str = json.dumps(payload_dict, separators=(',', ':'))
    edata_b = payload_str.encode('utf-8')
    key_b = key_str.encode('utf-8')
    encrypted = base64.b64encode(xor_str(edata_b, key_b))
    return url.quote(encrypted, safe="")

session = requests.Session()
session.verify = False  # Ignore SSL errors for testing

# Step 1: GET base URL
print("Step 1: GET base URL...")
try:
    r1 = session.get("https://iran.fruitcraft.ir/", timeout=10)
    print(f"Status: {r1.status_code}")
    print(f"Cookies: {dict(session.cookies)}")
    print(f"Headers received: {dict(r1.headers)}")
except Exception as e:
    print(f"Failed GET base URL: {e}")

# Step 2: POST with minimal params wrapped in V2 edata
print("\nStep 2: POST with minimal params...")
restore_key = input("Enter code (or leave blank to create new): ").strip()

payload = {
    'udid': 'android_test123',
    'game_version': '1.10.10755',
    'os_type': 2,
    'device_name': 'API_Test_Flow',
    'os_version': '10',
    'model': 'TestModel_API',
    'store_type': 'bazar'  # Trying 'bazar' instead of 'myket'
}
if restore_key:
    payload['restore_key'] = restore_key

# Encrypt the payload the exact same way the Lua client does it
edata_val = encrypt_v2(payload)
raw_body = f"edata={edata_val}&version=2"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; TestModel Build/QQ3A.200805.001)'
}

try:
    r2 = session.post("https://iran.fruitcraft.ir/player/load", data=raw_body, headers=headers, timeout=10)
    print(f"Status: {r2.status_code}")
    print(f"Response: {r2.text[:500]}")
except Exception as e:
    print(f"Failed POST to player/load: {e}")

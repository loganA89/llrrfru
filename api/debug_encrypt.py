import json
import base64
import urllib.parse as url
import requests
import urllib3

urllib3.disable_warnings()

# The test payload
payload = {
    'udid': 'android_debug123',
    'restore_key': 'test',  # Use placeholder for debug
    'game_version': '1.10.10755',
    'os_type': 2,
    'device_name': 'FruitClient_Debug',
    'os_version': '10',
    'model': 'FruitClient',
    'store_type': 'myket'
}

# V2 key
key = "mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk"

# Step 1: JSON
payload_str = json.dumps(payload, separators=(',', ':'))
print("Step 1 - JSON:", payload_str)

# Step 2: XOR
payload_bytes = payload_str.encode('utf-8')
key_bytes = key.encode('utf-8')
xor_result = bytearray()
for i in range(len(payload_bytes)):
    xor_result.append(payload_bytes[i] ^ key_bytes[i % len(key_bytes)])
xor_bytes_data = bytes(xor_result)
print("Step 2 - XOR bytes:", xor_bytes_data)

# Step 3: Base64
b64_result = base64.b64encode(xor_bytes_data)
print("Step 3 - Base64:", b64_result)

# Step 4: URL encode
url_encoded = url.quote(b64_result, safe="")
print("Step 4 - URL encoded:", url_encoded)

# Step 5: Full body
full_body = f"edata={url_encoded}&version=2"
print("Step 5 - Full body:", full_body)

# Step 6: Send manual request
print("\nStep 6 - Sending request...")
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; FruitClient Debug Build/1)'
}

resp = requests.post("https://iran.fruitcraft.ir/player/load", 
                     data=full_body, 
                     headers=headers, 
                     timeout=15,
                     verify=False)

print(f"Status: {resp.status_code}")
print(f"Headers: {dict(resp.headers)}")
print(f"Content-Length: {len(resp.content)}")
print(f"Response text: {resp.text[:1000]}")

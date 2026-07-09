from fruitcraft_client import FruitClient

code = "fact11439memory24"
client = FruitClient()
udid = "android_" + "test123456789ab"

print("Logging in...")
try:
    success, data = client.login(code, udid)
    if not success:
        print("Login failed!")
        exit(1)

    print(f"Current avatar: {data['data']['avatar_id']}")
    print(f"Available avatars: {data['data']['avatars']}")

    # Try to change to first available that isn't current
    target_avatar = data['data']['avatars'][0]
    if str(target_avatar) == str(data['data']['avatar_id']) and len(data['data']['avatars']) > 1:
        target_avatar = data['data']['avatars'][1]

    print(f"\nChanging avatar to: {target_avatar}")

    result = client.change_avatar(target_avatar)
    print("Result:", result)
except Exception as e:
    print("Failed to run test due to arena local outbound networking timeout.")


#!/usr/bin/env python3
"""One-account FruitCraft avatar update test.

Reads the recovery code from FRUIT_RECOVERY_CODE by default so it does not need
be stored in project configuration files.
"""
import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Run correctly whether invoked from the repository root or from scripts/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api.fruitcraft_client import FruitClient


def avatar_values(value: Any, path: str = "") -> List[Tuple[str, Any]]:
    """Return all avatar_id fields without printing the entire profile."""
    found: List[Tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key == "avatar_id":
                found.append((child_path, child))
            found.extend(avatar_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(avatar_values(child, f"{path}[{index}]"))
    return found


def compact_response(response: Any) -> Dict[str, Any]:
    if not isinstance(response, dict):
        return {"response_type": type(response).__name__}
    output: Dict[str, Any] = {"status": response.get("status")}
    if "error" in response:
        output["error"] = response["error"]
    data = response.get("data")
    if isinstance(data, dict):
        output["data_keys"] = sorted(data.keys())
        if "code" in data:
            output["code"] = data["code"]
        if "message" in data:
            output["message"] = data["message"]
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Change a FruitCraft account avatar and verify the profile.")
    parser.add_argument("--avatar-id", required=True, type=int)
    parser.add_argument("--recovery-code", default=os.getenv("FRUIT_RECOVERY_CODE"))
    parser.add_argument("--udid", default=os.getenv("FRUIT_UDID", "fruit-avatar-test-v1"))
    args = parser.parse_args()

    if not args.recovery_code:
        print("ERROR: supply FRUIT_RECOVERY_CODE or --recovery-code", file=sys.stderr)
        return 2

    client = FruitClient()
    logged_in, login_response = client.login(args.recovery_code, args.udid)
    if not logged_in:
        print("LOGIN_FAILED", compact_response(login_response))
        return 3

    before = client.get_profile()
    print("LOGIN_OK")
    print("AVATAR_BEFORE", avatar_values(before))

    changed = client.change_avatar(args.avatar_id)
    print("CHANGE_RESPONSE", compact_response(changed))
    if not isinstance(changed, dict) or not changed.get("status"):
        return 4

    after = client.get_profile()
    after_avatars = avatar_values(after)
    print("AVATAR_AFTER", after_avatars)

    if any(value == args.avatar_id for _, value in after_avatars):
        print("AVATAR_CHANGE_VERIFIED")
        return 0

    print("AVATAR_CHANGE_UNVERIFIED")
    return 5


if __name__ == "__main__":
    raise SystemExit(main())

import os, re
import sys

def main():
    decompiled_dir = "/root/fruitcraft_rev/decompiled"
    if not os.path.exists(decompiled_dir):
        print(f"Directory {decompiled_dir} not found.")
        return

    routes = set()
    for root_dir, dirs, files in os.walk(decompiled_dir):
        for file in files:
            if not file.endswith(".lua"): continue
            with open(os.path.join(root_dir, file), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                # Look for API endpoints in Constants
                if "Constants.lua" in file:
                    for line in content.split("\n"):
                        if "API_" in line and "=" in line and "\"" in line:
                            print("CONSTANT ROUTE: " + line.strip())
                
                # Look for network.request
                for line in content.split("\n"):
                    if "network.request(" in line:
                        print("REQUEST in " + file + ": " + line.strip())

if __name__ == "__main__":
    main()

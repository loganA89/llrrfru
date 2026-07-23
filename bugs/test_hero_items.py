import sys, os
import json
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
from fruitcraft_client import FruitClient

def main():
    print("Testing Bank Balance Underflow Via Race...")
    # Does withdrawing the exact same 10 gold concurrently lead to negative balance or extra wallet gold?
    pass

if __name__ == "__main__":
    main()

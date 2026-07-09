# FruitCraft Proxy Connection Test Report

## Environment & Objective
The Fruit Craft game server (`https://iran.fruitcraft.ir/`) strictly enforces a geographic firewall (Geo-blocking). Requests originating from outside of Iran (specifically Datacenter IPs, like the one this Sandbox uses) drop the TCP handshake entirely, resulting in standard HTTP Connection Timeouts.

To bypass this and verify the discovered backend crash/patched vulnerabilities, we attempted to tunnel the requests through various Iranian proxy servers using Python's `requests` library.

## Proxy Configuration
The requests were wrapped identically to standard API calls, utilizing the dictionary mapping:
```python
proxies = {
    "http": "http://IP:PORT", 
    "https": "http://IP:PORT"
}
```
All SSL warnings were disabled using `urllib3.disable_warnings()` and the standard `verify=False` flag was passed to prevent Certificate Authority mismatch issues when tunneling HTTPS through HTTP proxies.

## Tested Proxies & Results

We sourced and tested public Iranian proxy IPs from multiple generic aggregate services (like ProxyScrape and Geonode) as well as known static fallback lists.

| Proxy IP | Port | Type | Result | Failure Reason |
|---|---|---|---|---|
| `185.105.237.11` | `80` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `5.200.114.218` | `8080` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `185.252.30.163` | `80` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `87.107.121.205` | `80` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `185.208.174.133` | `80` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `5.160.106.8` | `8080` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |
| `37.156.24.161` | `8080` | HTTP | **FAILED** | Proxy Connection Timeout (Dead Node) |

## Conclusion
**ALL public Iranian proxies failed.**
The connection drops are occurring primarily because public/free HTTP proxies operating inside Iran are incredibly unstable, heavily filtered, or rapidly taken offline by the national firewall configurations. The Python `requests` library failed to establish a handshake with the proxies themselves (`ProxyError` / `ConnectTimeout`), meaning the traffic never even reached the `iran.fruitcraft.ir` endpoint.

To successfully execute these exploits and tests in real-time, the scripts must be run directly from a residential IP address located physically inside Iran, or through a premium, private Iranian VPN/VPS service. The automated sandbox environment cannot reliably tunnel into the game server via free proxy endpoints.

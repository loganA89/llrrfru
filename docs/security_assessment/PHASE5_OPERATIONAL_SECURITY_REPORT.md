# Phase 5: Operational Security & Infrastructure Surface Assessment

## Executive Summary
Phase 5 shifted focus away from the game's business logic and evaluated the operational security, client exposure, and infrastructure hygiene of the live FruitCraft backend (`iran.fruitcraft.ir`). We assessed the HTTP layer, web application firewall (WAF) routing, internal data leaks, legacy interfaces, and error handling mechanisms to determine the overall attack surface available to an external threat actor.

**NO HIGH-IMPACT VULNERABILITY CONFIRMED.**
There are no remotely exploitable administrative interfaces, wide-open network ports, or leaked private keys granting unauthenticated backend control. However, there are systemic weaknesses in the Zend framework error handling that disclose infrastructure paths.

---

## 1. Confirmed Operational Security Weaknesses

### 1.1 WAF/Proxy Headers Bypassed
- **Description:** The backend API accepts and processes standard user requests without sanitizing proxy headers like `X-Forwarded-For`.
- **Finding Details:** We proved that injecting an arbitrary `X-Forwarded-For` header (`8.8.8.8`) into a valid request successfully routes through the nginx/WAF layers without rejection. 
- **Impact:** Low. The system does not appear to trust this header for authorization bypass (as proved in Phase 2), but it means IP-based rate limiting or logging could be easily polluted or bypassed by an attacker rotating this header dynamically.

### 1.2 Administrative Interface Exposure & Legacy Routing
- **Description:** The backend hosts an exposed legacy admin portal on the primary web server at `GET /admin/login`.
- **Finding Details:** We mapped this route from source code hints and web-layer probing. The portal returns an HTML interface (`<title>Fruit Admin</title>`). We tested basic credential stuffing and SQL injection (`admin' OR '1'='1`).
- **Impact:** Secure/Mitigated. The portal successfully defends against basic SQLi and default credential attacks. It returns a `302 Redirect` back to the login page on failure without dumping database errors. However, exposing backend administrative panels to the public internet violates defense-in-depth principles.

### 1.3 Denial of Service (DoS) via Infrastructure Stack Tracing
- **Description:** As previously identified, the backend lacks global JSON exception handling. Structural mismatches generate fatal Zend Engine errors.
- **Finding Details:** Because this error is rendered as a complete HTML response rather than a lightweight 400 Bad Request JSON, the server wastes significant computational power generating stack frames.
- **Impact:** Medium. This is a severe operational risk for server availability. An attacker can repeatedly send `{"withdraw": [100]}` to force the PHP-FPM process to crash and generate heavy HTML dumps, likely leading to resource exhaustion (CPU/Memory) if scaled via a botnet.

### 1.4 Client-Side Exposure (V2 Encryption Keys)
- **Description:** The custom XOR cipher key (`mwBSDp1nMhcdCravltVGADXTFx7bN9mr0XMgyDezIJghf65lvXhRdLWrScCk`) is hardcoded within the decompiled Lua client (`Utils.Toolbox.lua`).
- **Finding Details:** This is **intended public client material**. Because the key is static and universal to all clients, it provides security through obscurity rather than true cryptographic protection.
- **Impact:** Informational. Extracting this key is trivial for anyone decompiling the APK (as done in this project), enabling man-in-the-middle decryption of all API traffic or the creation of custom automation clients.

---

## 2. Infrastructure Surface Map
- **Target Host:** `iran.fruitcraft.ir` (Resolved IP: `185.120.220.199`)
- **Transport Security:** TLSv1.2 (ECDHE-RSA-AES256-GCM-SHA384) active on port 443. The certificate is a standard Let's Encrypt CA. Port 80 redirects or serves generic nginx 403s.
- **Reverse Proxy / Load Balancer:** `nginx/1.21.3`
- **Application Engine:** PHP (`x-powered-by: PHP/7.4.33` or `PHP/7.1.33` depending on the route).

## 3. Recommended Remediation Plan
1. **Remove Admin Portals from Public Internet:** Access to `/admin/login` should be restricted at the nginx level to authorized VPN/IP ranges only.
2. **Global Exception Handling:** Patch the Zend framework's `exception_handler` to intercept `TypeError` or array-indexing failures. It must return a unified, static JSON error string instead of an HTML stack trace to mitigate the DoS risk.
3. **Drop Spoofed Headers:** Configure the edge nginx servers to aggressively strip or overwrite client-provided `X-Forwarded-For` headers to ensure accurate security logging.

---
*All analytical data from Phase 5 has been synchronized.*

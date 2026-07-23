# Phase 5: Infrastructure & Operational Remediation Plan

## Overview
While the core business logic of FruitCraft successfully prevents database-level currency or item exploits, the operational infrastructure requires hardening to prevent Denial of Service (DoS) and restrict administrative attack surfaces.

## 1. Zend Framework Exception Handling (High Priority)
**The Problem:** Unhandled type mismatches (e.g. injecting arrays into string fields) cause the PHP backend to crash and render a computationally heavy HTML stack trace. This poses a significant DoS risk to the PHP-FPM worker pools.
**The Fix:** 
- Implement a global `try/catch` block or custom exception handler in the root API router.
- When a `TypeError` occurs, the handler must `return json_encode(['status' => false, 'error' => 'Bad Request']);` and terminate cleanly.

## 2. Administrative Interface Isolation (Medium Priority)
**The Problem:** The portal at `https://iran.fruitcraft.ir/admin/login` is accessible from the public internet.
**The Fix:**
- Update the Nginx configuration to block access to `/admin/*` via an `allow/deny` block.
- Require internal VPN access or an IP whitelist to reach backend maintenance panels.

## 3. Nginx WAF & Header Sanitization (Low Priority)
**The Problem:** The server accepts and likely logs arbitrary `X-Forwarded-For` and `Client-IP` headers injected by the client, allowing IP spoofing in application logs.
**The Fix:**
- Configure Nginx to strip untrusted `X-Forwarded-For` headers.
- Remove the `x-powered-by: PHP/7.4.33` header to reduce information disclosure regarding the backend technology stack.

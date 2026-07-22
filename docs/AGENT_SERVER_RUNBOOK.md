# FruitCraft Iran Cloud Server — Agent & Developer Runbook

**Last verified:** 2026-07-22  
**Purpose:** Give an authorized engineering agent or developer reliable operational context for the FruitCraft automation server.  
**Classification:** Operationally sensitive. Do **not** commit credentials, API tokens, SSH private keys, account cookies, or CAPTCHA credentials to Git.

---

## 1. Architecture and Objective

The game-facing worker **must remain in Iran** because it must reach the FruitCraft Iran service.

```text
Authorized agent/developer
        │
        │ SSH through an outbound reverse TCP tunnel
        ▼
Iran cloud server (Ubuntu / ParsPack)
        │
        ▼
FruitCraft Iran service
```

The Iran cloud server is the execution environment for all real network tests, client debugging, and automation runs. It is not a disposable development machine.

### Why the tunnel is required

Direct SSH from the agent environment to the Iran server was not reliable. A packet capture on the server showed that packets from the agent did not arrive during a direct test. This is a route / egress-path issue, not a Python, SSH-key, or Ubuntu issue.

The working pattern is therefore **outbound-first**: the Iran server creates a reverse tunnel to an Internet relay, then the agent connects to the relay endpoint.

---

## 2. Current Server Inventory

| Item | Verified value |
|---|---|
| Provider | ParsPack cloud server |
| Server hostname | `srv4534225212` |
| Operating system | Ubuntu 22.04.5 LTS |
| Kernel | Linux 5.15.0-186-generic, x86_64 |
| Project path | `/root/llrrfru` |
| Project branch | `main` |
| Last verified commit | `c489d26` — `Test: Quest with old encryption format` |
| Python runtime | `/root/llrrfru/venv/bin/python` — Python 3.10.12 |
| SSH listeners | TCP 22 and TCP 443, IPv4 and IPv6 |

### Project structure

```text
/root/llrrfru/
├── api/
│   ├── account_manager.py
│   ├── captcha_solver.py
│   ├── config.json
│   ├── fruitcraft_client.py
│   └── session_manager.py
├── docs/
├── scripts/
│   ├── quest_bot.py
│   └── shop_buy.py
├── bugs/
├── main_menu.py
└── venv/
```

The Git remote is the repository referenced by the project owner. Never put a personal access token into the remote URL.

---

## 3. Current Working Access Method

### Temporary reverse SSH tunnel

A Pinggy TCP reverse tunnel was successfully created from the Iran server using outbound TCP port 443.

Server-side command:

```bash
ssh -p 443 \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -R0:localhost:22 \
  tcp@free.pinggy.io
```

The command prints a temporary endpoint in this form:

```text
tcp://HOST:PORT
```

Agent/developer connection pattern:

```bash
ssh -p PORT -i AGENT_PRIVATE_KEY root@HOST
```

### Verified result

The agent successfully authenticated with its SSH key and executed:

```text
SSH_OK
srv4534225212
root
/root
```

### Important tunnel rules

1. Keep the Pinggy terminal process open; do not press `Ctrl+C`.
2. The free tunnel expires after approximately 60 minutes.
3. The free endpoint changes when the tunnel restarts.
4. Do not publish the endpoint in public repositories, tickets, or screenshots.
5. Do not use the root password through a public tunnel. Use the authorized SSH key.

---

## 4. Permanent Access Design

The temporary Pinggy tunnel proves the correct network architecture: **server-initiated connection over TCP 443**.

For long-lived access, use a persistent outbound tunnel service or relay with all of the following properties:

- outbound connection from the Iran server over TCP 443 or another proven reachable egress path;
- fixed endpoint or a safe discovery mechanism;
- automatic reconnect after reboot;
- SSH-key-only authentication;
- no dependency on an agent source IP allowlist.

### Do not use as the permanent control plane

- Direct inbound SSH to the Iran server: not reliable from the agent network.
- ParsPack API token with one allowed source IP: the agent egress IP changes dynamically.
- Unauthenticated public tunnel endpoints.
- Password-based root SSH access.

### Recommended persistence checklist

1. Use a service tier / relay that offers a stable TCP endpoint.
2. Create a systemd service to maintain the outbound tunnel and restart it automatically.
3. Store any tunnel credential in a root-only file, mode `0600`.
4. Restrict SSH to public-key authentication before exposing a stable endpoint.
5. Add a health check that verifies the tunnel and alerts on reconnect / endpoint change.

---

## 5. SSH and Firewall State

### SSH

The server is listening on both ports:

```text
0.0.0.0:22
0.0.0.0:443
[::]:22
[::]:443
```

Configured SSH drop-in files include:

```text
/etc/ssh/sshd_config.d/90-agent-key-only.conf
/etc/ssh/sshd_config.d/91-ssh-ports.conf
```

**Security audit required:** an effective SSH configuration check reported password authentication as enabled even though a drop-in intends to disable it. Before creating a permanent public endpoint, verify and correct it.

Verification command:

```bash
sshd -T | grep -E '^(port|permitrootlogin|passwordauthentication|pubkeyauthentication) '
```

Expected secure baseline:

```text
permitrootlogin without-password
pubkeyauthentication yes
passwordauthentication no
```

### UFW

UFW is active. Its current rule list contains a broad allow rule equivalent to allowing traffic from anywhere. This should be reviewed before any permanent public endpoint is deployed.

Audit command:

```bash
ufw status numbered
```

Do not delete firewall rules remotely until there is a verified recovery path through the Web Console.

### ParsPack cloud firewall

The ParsPack cloud firewall was configured with explicit incoming SSH-related rules during troubleshooting. The current tunnel does not require inbound access to the Iran server; it uses outbound TCP 443 instead.

---

## 6. Service and Cleanup State

### Cloudflared

A `cloudflared` service is enabled but repeatedly exits with status `255` because of prior incomplete tunnel configuration.

Current state at verification:

```text
cloudflared.service: activating (auto-restart)
exit status: 255
```

It is unrelated to the working Pinggy access path. After preserving any logs needed for debugging, disable it to stop repeated restart noise:

```bash
systemctl disable --now cloudflared
```

### Legacy ParsPack API bootstrap

A temporary bootstrap process was created during an unsuccessful API-control experiment:

```text
/usr/local/sbin/fruit-bootstrap.py
/var/lib/fruit-agent/bootstrap-error.log
```

It is not the working access path. It logged HTTP 403 responses and should be removed after confirming that SSH tunnel access is stable.

Suggested cleanup, only after approval:

```bash
pkill -f '^python3 /usr/local/sbin/fruit-bootstrap.py$' || true
rm -f /usr/local/sbin/fruit-bootstrap.py
rm -rf /var/lib/fruit-agent
```

---

## 7. Safe Developer Workflow

After connecting through the tunnel:

```bash
cd /root/llrrfru
/root/llrrfru/venv/bin/python --version
git status --short
git log -1 --oneline
```

Basic bot startup check:

```bash
cd /root/llrrfru
/root/llrrfru/venv/bin/python scripts/quest_bot.py
```

At the last verification, the bot started but reported no active accounts. Do not add account secrets to Git, shell history, screenshots, or this document.

### Current Git hygiene warning

At the last verification, `api/accounts.json` existed as an **untracked** file. Treat it as sensitive account configuration. Do not add it to Git. Add an appropriate ignore rule before making project commits.

### Change discipline

1. Inspect before editing.
2. Make a Git commit before a risky functional change.
3. Run a dry / low-rate test with one test account first.
4. Preserve request / response logs with secrets redacted.
5. Increase automation rate only after a successful controlled test.
6. Never use exploit files under `bugs/` against production accounts without explicit approval.

---

## 8. FruitCraft Project Context

Known project goals:

- Python-only backend automation;
- V2 encryption support;
- Quest / mission automation;
- CAPTCHA handling;
- rate-limit management;
- multi-account support.

Known code locations:

```text
api/fruitcraft_client.py
scripts/quest_bot.py
api/account_manager.py
api/session_manager.py
api/captcha_solver.py
```

Known previous result: the server can reach the FruitCraft Iran service, while the agent environment cannot reliably reach that service directly. Execute real game-facing tests from this Iran cloud server only.

---

## 9. Credential and Incident Rules

Credentials were previously pasted into chat and screenshots during access troubleshooting. Treat all such credentials as exposed.

Required rotation list:

1. Root password.
2. ParsPack cloud-storage credentials.
3. Temporary ParsPack API tokens.
4. Any Cloudflare tunnel token that appeared in terminal output or files.
5. Any temporary tunnel endpoint / access token after the session ends.

Never place secrets in:

```text
Git history
README files
Markdown runbooks
shell history
screenshots
systemd unit files with world-readable permissions
```

Use root-only secret files:

```bash
install -d -m 700 /root/.secrets
install -m 600 /dev/null /root/.secrets/service-token
```

---

## 10. Handover Checklist

Before an agent or developer starts work, confirm:

- [ ] A live reverse-tunnel endpoint is available.
- [ ] SSH key authentication succeeds.
- [ ] Tunnel terminal / service is still running.
- [ ] Repository is clean or changes are understood.
- [ ] Python virtual environment is available.
- [ ] No secrets will be printed in command output.
- [ ] The work is happening on `/root/llrrfru`, not an unrelated copy.
- [ ] A single-account, low-rate validation plan exists before live automation.

Before ending work:

- [ ] Save relevant logs with secrets redacted.
- [ ] Commit intentional code changes.
- [ ] Record any running service or tunnel process.
- [ ] Close temporary tunnels if they are no longer required.
- [ ] Rotate temporary credentials that were shared during the session.

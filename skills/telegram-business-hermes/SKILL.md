---
name: telegram-business-hermes
description: "Use when configuring, patching, debugging, or documenting Hermes Agent support for Telegram Business delegated inbox / Business Bot API: direct bot replies in 1-to-1 Business chats, operator-only mention/reply triggers, trusted operator full mode, external contact web-only safe mode, business_connection_id propagation, and secret-free setup templates."
---

# telegram-business-hermes

Use this skill to reproduce the Telegram Business delegated inbox setup for
Hermes without copying secrets or server-local state.

## Safety Model

- Treat Telegram Business delegated inbox as two audiences in the same transport.
- Trusted operator: full Hermes mode, normal tools, memory, files, and terminal according to the profile.
- External Business contact: web-only safe mode; allow only public `web_search` and `web_extract`.
- Never treat wildcard allow-all settings as Business trust. Trust must come from explicit user IDs or an approved pairing store.
- Preserve `business_connection_id` from inbound update to outbound Telegram send kwargs. Losing it commonly causes `Forbidden: bot can't initiate conversation with a user`.

## Patch Workflow

Apply the bundled patch only when the target Hermes checkout does not already
contain equivalent Telegram Business delegated inbox support.

```bash
git am skills/telegram-business-hermes/patches/telegram-business-delegated-inbox.patch
```

The patch was generated from upstream work proposed in:

- Issue: https://github.com/NousResearch/hermes-agent/issues/26653
- PR: https://github.com/NousResearch/hermes-agent/pull/26654

If the PR is already merged in the target Hermes version, prefer updating
Hermes normally and use this skill only for configuration and verification.

## Telegram Setup

1. In BotFather, enable `Bot Settings -> Business Mode`.
2. In the Telegram Business account, connect the bot under `Telegram Business -> Chatbots`.
3. Grant read and reply rights.
4. Ensure the target 1-to-1 chats are not excluded.
5. Keep bot tokens, operator IDs, and auth stores outside this repository.

## Configuration

Load the secret-free template when you need exact YAML shape:
`references/telegram-business-config.example.yaml`.

Minimum profile shape:

```yaml
telegram:
  require_mention: true
  mention_patterns:
    - (?i)\bsigurd\b
  business:
    enabled: true
    trigger_words:
      - Sigurd
      - Сигурд
    allowed_chats: []
    cooldown_seconds: 2.0
```

Minimum environment shape:

```bash
TELEGRAM_BOT_TOKEN=replace_with_telegram_bot_token
TELEGRAM_ALLOWED_USERS=replace_with_operator_telegram_user_id
```

Do not use `TELEGRAM_ALLOW_ALL_USERS=true`, `GATEWAY_ALLOW_ALL_USERS=true`, or
`*` as evidence that a Business sender is trusted.

## Expected Behavior

- Operator in a delegated Business DM says `Sigurd, status`: Hermes runs in full mode.
- External contact says `Sigurd, find public information about X`: Hermes runs web-only.
- External contact sends a message without trigger/reply: Hermes ignores it.
- Replies in Business chats are sent with `business_connection_id`.
- The “open chat with human/operator” CTA is shown only for external Business contact responses, not for normal operator messages.

## Verification

Run syntax and focused tests in the Hermes checkout:

```bash
python -m py_compile gateway/platforms/telegram.py gateway/platforms/base.py gateway/session.py gateway/run.py gateway/config.py
python -m pytest tests/gateway/test_telegram_business.py tests/gateway/test_telegram_thread_fallback.py -q -o addopts=
```

For a live gateway restart initiated from Telegram, use no-block systemd:

```bash
sudo systemctl --no-block restart hermes-gateway.service
```

Check logs for separate inbound, generation, and delivery states:

- `Received Telegram Business message update`
- `Accepted Telegram Business message`
- `Ignored Telegram Business message ... reason=missing_trigger`
- `Failed to send Telegram message: Forbidden: bot can't initiate conversation with a user`

Diagnose `missing_trigger` separately from outbound delivery failures. An
accepted message can still fail later if `business_connection_id` is lost or
Telegram has not granted `can_reply`.

## Public Release Checklist

- No `.env`, tokens, auth stores, logs, session dumps, or real chat/user IDs.
- Only placeholders in config and docs.
- Run the repository scanner before publishing:

```bash
python scripts/scan-secrets.py .
```

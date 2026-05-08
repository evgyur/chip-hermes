# chip-hermes

Public, secret-free Hermes profile templates for Chip-style Telegram agents.

This repository captures the safe parts of the Hermes setup:

- MiniMax `mmfast` default model with high reasoning behavior.
- `gptt` model alias for GPT thinking sessions.
- `gptprof-hermes` skill for profile/debug work.
- Groq speech-to-text for Telegram voice messages.
- MiniMax Token Plan MCP image understanding through `understand_image`.
- Cognee-ready memory settings with isolated per-user runtime roots.

It intentionally does not contain live tokens, private chat IDs, database
passwords, production `.env` files, or copied server state.

## Repository Layout

```text
config/
  hermes.config.example.yaml
  env.example
  systemd/hermes-gateway.service.example
docs/
  models.md
  media.md
  memory.md
  deployment.md
skills/
  gptprof-hermes/SKILL.md
scripts/
  scan-secrets.py
```

## Quick Start

1. Copy `config/hermes.config.example.yaml` to the target user's Hermes home as
   `config.yaml`.

2. Copy `config/env.example` to the target Hermes home as `.env`.

3. Fill secrets only on the server:

   ```bash
   HERMES_HOME=/home/<user>/.hermes
   install -m 0600 config/env.example "$HERMES_HOME/.env"
   editor "$HERMES_HOME/.env"
   ```

4. Install the MiniMax MCP wrapper for the runtime user.

5. Run the Hermes doctor and MCP smoke checks from `docs/deployment.md`.

6. Before publishing changes, run:

   ```bash
   python scripts/scan-secrets.py .
   ```

## Public Safety Contract

- Keep only placeholders in this repository.
- Never commit `.env`, `auth.json`, `auth-profiles.json`, session stores, logs,
  Telegram update dumps, or Cognee databases.
- Treat all real model keys as server-local secrets.
- Treat all private dialogue memory as non-public data.

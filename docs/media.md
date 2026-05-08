# Media Understanding

Hermes should convert voice and images into text before the main MiniMax
conversation. This keeps the primary dialogue model simple and allows each
media provider to be tested separately.

## Voice Through Groq

Template:

```yaml
stt:
  provider: groq
  model: whisper-large-v3-turbo
  api_key_env: GROQ_API_KEY
```

Operational notes:

- Put `GROQ_API_KEY` only in `$HERMES_HOME/.env`.
- Keep transcription output short and pass it to the main turn as user text.
- If the bot goes silent after a voice message, check Telegram polling and
  gateway logs before blaming STT.

## Images Through MiniMax MCP

Template:

```yaml
agent:
  image_input_mode: text

auxiliary:
  vision:
    provider: minimax_mcp
    mcp_server: minimax-coding-plan
    tool: understand_image
    api_key_env: MINIMAX_API_KEY
```

Wrapper pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$HOME"
exec "$HOME/.local/bin/uvx" minimax-coding-plan-mcp -y
```

Operational notes:

- Put the wrapper at `$HOME/.local/bin/minimax-mcp-wrapper`.
- Make it executable with `chmod 0755`.
- Put `MINIMAX_API_KEY` only in `$HERMES_HOME/.env`.
- The MiniMax Token Plan key must be a real Token Plan key; a short chat model
  key may not work for `/v1/coding_plan/vlm`.

Smoke check:

```bash
sudo -u hermes env HOME=/home/hermes HERMES_HOME=/home/hermes/.hermes \
  PATH=/home/hermes/.local/bin:/usr/local/bin:/usr/bin:/bin \
  /opt/hermes-agent/venv/bin/python -m hermes_cli.main mcp test minimax-coding-plan
```

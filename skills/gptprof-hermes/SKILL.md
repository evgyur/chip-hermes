---
name: gptprof-hermes
description: Use when configuring, profiling, debugging, or documenting a Hermes Telegram profile that uses MiniMax mmfast, GPT thinking aliases, Groq voice transcription, MiniMax MCP image understanding, or Cognee memory.
---

# gptprof-hermes

Use this skill for Hermes profile work: model routing, media input checks,
memory boundaries, and safe public documentation.

## Operating Contract

1. Identify the target profile and `$HERMES_HOME`.
2. Confirm which model alias is active: `mmfast` or `gptt`.
3. Check media routes separately:
   - voice: Groq STT
   - images: MiniMax MCP `understand_image`
4. Check memory separately:
   - fast session recall
   - Cognee graph/vector persistence
5. Never print or copy secrets.
6. Before publishing docs or configs, run the repository secret scanner.

## Model Defaults

- `mmfast`: MiniMax `MiniMax-M2.7-highspeed`, high reasoning, default Hermes conversation.
- `gptt`: OpenAI Codex GPT thinking alias, high reasoning, only when Codex auth is available.

## Voice Check

Verify configuration shape:

```yaml
stt:
  provider: groq
  api_key_env: GROQ_API_KEY
```

If a voice message is silent, inspect Telegram gateway/polling logs before
assuming Groq failed.

## Image Check

Verify configuration shape:

```yaml
agent:
  image_input_mode: text
auxiliary:
  vision:
    provider: minimax_mcp
    tool: understand_image
```

Run the MCP test for `minimax-coding-plan` under the target Unix user.

## Memory Check

Verify configuration shape:

```yaml
memory:
  provider: cognee
  memory_enabled: true
plugins:
  cognee:
    runtime_dir: $HERMES_HOME/cognee
```

Do not point two private bots at the same Cognee runtime root unless that is an
explicit product decision.

## Public Documentation Checklist

- No `.env`.
- No tokens.
- No auth stores.
- No session logs.
- No Cognee data.
- Only placeholders and operational patterns.

# Models

## `mmfast`

Default Hermes model alias:

```yaml
model:
  provider: minimax
  alias: mmfast
  id: MiniMax-M2.7-highspeed
  reasoning: high
```

Use `mmfast` for normal Telegram conversation where the bot should stay fast
but still reason carefully. The public template sets `reasoning: high`; adapt
the exact field name to the Hermes/OpenClaw runtime version if it changes.

## `gptt`

Thinking alias for Codex-backed GPT sessions:

```yaml
model_aliases:
  gptt:
    provider: openai-codex
    id: gpt-5.4
    reasoning: high
```

Use `gptt` for deeper reasoning sessions when OAuth-backed Codex auth is
available in the target runtime. Do not commit OAuth stores or auth profiles.

## Safety

- Keep model IDs and aliases public.
- Keep keys private.
- Keep OAuth stores private.
- Keep provider-specific account IDs private unless deliberately published.

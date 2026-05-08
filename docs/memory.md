# Memory

This template is Cognee-ready but does not include any private memory data.

Recommended profile-local root:

```yaml
memory:
  provider: cognee
  memory_enabled: true
  user_profile_enabled: true
  live_recall_scope: session

plugins:
  cognee:
    runtime_dir: $HERMES_HOME/cognee
    dataset: hermes-dialogues
    session_id: hermes-global-dialogues
```

Rules:

- Each Telegram persona/user should have an isolated `$HERMES_HOME`.
- Do not share Cognee runtime roots between unrelated bots.
- Do not commit Cognee databases, graph stores, Lance vector stores, caches, or
  raw dialogue transcripts.
- Live Telegram replies should prefer fast session recall. Full graph recall is
  useful for maintenance, but it can be heavier and should not block every turn.

# Deployment Notes

This is a template for a Linux systemd Hermes deployment.

## Install Shape

```text
/opt/hermes-agent
  venv/
  hermes_cli/
  tools/

/home/hermes/.hermes
  config.yaml
  .env
  cognee/
  minimax-mcp/
```

## Steps

1. Create a dedicated Unix user.

2. Install Hermes under `/opt/hermes-agent`.

3. Copy `config/hermes.config.example.yaml` to
   `/home/hermes/.hermes/config.yaml`.

4. Copy `config/env.example` to `/home/hermes/.hermes/.env` and fill secrets on
   the server only.

5. Install `$HOME/.local/bin/minimax-mcp-wrapper`.

6. Install a systemd unit based on
   `config/systemd/hermes-gateway.service.example`.

7. Verify:

```bash
systemctl status hermes-gateway.service --no-pager -l
sudo -u hermes env HOME=/home/hermes HERMES_HOME=/home/hermes/.hermes \
  PYTHONPATH=/opt/hermes-agent \
  /opt/hermes-agent/venv/bin/python -m hermes_cli.main doctor
sudo -u hermes env HOME=/home/hermes HERMES_HOME=/home/hermes/.hermes \
  PATH=/home/hermes/.local/bin:/usr/local/bin:/usr/bin:/bin \
  /opt/hermes-agent/venv/bin/python -m hermes_cli.main mcp test minimax-coding-plan
```

## Public Repo Rule

Before pushing:

```bash
python scripts/scan-secrets.py .
git status --short
git diff --cached
```

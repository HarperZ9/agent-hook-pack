# agent-hook-pack

`agent-hook-pack` is a small, public-safe hook pack for local development
workflows that need basic guardrails without importing a private automation
stack.

Included hooks:

- `block-secrets.py`
- `check-branch.sh`
- `check-env-sync.sh`
- `verify-no-secrets.sh`
- `lint-on-save.sh`

Use it when you want lightweight secret checks, branch guardrails, env-template
sync checks, and consistent hook deployment.

Built with agentic tooling and manually reviewed before publish.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
agent-hook-pack audit
agent-hook-pack list
agent-hook-pack install --target .claude/hooks
agent-hook-pack path
```

## Note

The hooks are generic, intentionally scoped, and omit private policy layers.

# Settings & Hooks Configuration — Reference

<!--
  PLACEMENT: this is a REFERENCE doc for the agent. Save it at:
    docs/setup/enforcement-config.md
  The agent must TRANSLATE the JSON blocks below into the real files:
    - deny rules  → ~/.claude/settings.json   (user scope, applies everywhere)
    - hooks       → .claude/settings.json      (workspace scope) OR ~/.claude/settings.json
  Do NOT commit secrets. Show Sergio the diff and wait for approval before writing
  to any settings.json (per the constitution + handoff instructions).
-->

This document specifies the deterministic enforcement layer: `deny` permission
rules and `PreToolUse` hooks. It is the companion to `constitution.md` — the
constitution states the *law* (probabilistic guidance); this config *enforces* it
(deterministic, runs as code every time).

## 1. Deny rules — `~/.claude/settings.json` (user scope)

Placed at user scope so they apply across every project, including Kibo (whose
own `.git` would otherwise cut off workspace-level `.claude/` config).

```json
{
  "permissions": {
    "deny": [
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/credentials*.json)",
      "Read(**/.git/config)",
      "Edit(**/.env*)",
      "Edit(**/decisions.json)"
    ],
    "ask": [
      "Bash(git push:*)"
    ],
    "defaultMode": "default"
  }
}
```

Notes for Sergio (learning):
- `deny` always wins over `ask` and `allow`; first match decides.
- `Edit(**/decisions.json)` protects Kibo's locked design system (24 decisions).
- `ask(Bash(git push:*))` makes Claude pause and ask before pushing.
- These rules MERGE with any existing settings.json — the agent must not clobber
  current keys; it should add to `permissions`, preserving the rest.

## 2. Hook registration — `.claude/settings.json`

Registers the two guard scripts. `$CLAUDE_PROJECT_DIR` resolves to the project
root so the path works regardless of the current working directory.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/secret-scan.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/sql-guard.sh"
          }
        ]
      }
    ]
  }
}
```

Why `PreToolUse` and why this matters:
- `PreToolUse` runs BEFORE the tool executes and can BLOCK it by exiting with
  code `2`. This evaluation happens before the permission mode, so it cannot be
  bypassed — even in a permissive mode.
- The `matcher` is a regex over the tool name: `Edit|Write` fires the secret scan
  on any file write; `Bash` fires the SQL guard on any shell command.

## 3. How to test the hooks (mini smoke test)

After the scripts exist and are executable (`chmod +x`):
1. Secret scan: ask Claude to write a file containing `sk-test123` or a fake
   connection string → the Edit/Write must be BLOCKED.
2. SQL guard: ask Claude to run a Bash command containing `DROP TABLE foo` →
   the Bash call must be BLOCKED.
3. Negative control: a normal `Write` of plain text and a normal `Bash ls` must
   PASS, proving the hooks are not over-blocking.

## 4. Where each law is enforced (mapping)

| Law (constitution)              | Text guidance | Deterministic enforcement                       |
|---------------------------------|---------------|-------------------------------------------------|
| No secrets in code (Art. 1)     | Yes           | deny `Read/Edit(.env*)` + `secret-scan.sh`      |
| Read-only production DB (Art. 2)| Yes           | `sql-guard.sh` + read-only MCP                  |
| Locked design files (Art. 9)    | Yes           | deny `Edit(decisions.json)`                     |
| Financial redaction (Art. 3)    | Yes           | text only (hard to force 100%); no auto-memory  |
| Language rules (Art. 7)         | Yes           | text only                                       |

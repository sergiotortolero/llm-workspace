#!/usr/bin/env bash
# PLACEMENT: .claude/hooks/sql-guard.sh   (chmod +x after creating)
# PURPOSE: PreToolUse hook for Bash. Blocks destructive SQL keywords so that
#          client/production databases stay read-only by default (Constitution
#          Article 2). Exit 2 = BLOCK. Exit 0 = allow.
#
# Learning note (for Sergio):
#   - This guards the Bash tool specifically. If Claude tries to run sqlcmd /
#     psql / a python script whose command line contains a destructive verb,
#     this hook stops it before execution.
#   - It is intentionally conservative: it matches whole-word SQL verbs so that
#     innocent words (e.g. "updated_at") do not trigger a false block.
#   - To AUTHORIZE a specific write, Sergio removes/relaxes this guard for that
#     task, or sets the env var SQL_WRITE_AUTHORIZED=1 for the session.

set -euo pipefail

# Escape hatch: explicit, per-session authorization.
if [[ "${SQL_WRITE_AUTHORIZED:-0}" == "1" ]]; then
  exit 0
fi

payload="$(cat)"

if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"
else
  cmd="$payload"
fi

# Whole-word, case-insensitive match on destructive verbs.
destructive='(^|[^A-Za-z_])(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|EXEC|EXECUTE|GRANT|REVOKE|MERGE)([^A-Za-z_]|$)'

if printf '%s' "$cmd" | grep -Eiq "$destructive"; then
  echo "BLOCKED by sql-guard.sh: command contains a destructive SQL keyword." >&2
  echo "Production data is read-only by default (Constitution Article 2)." >&2
  echo "If this write is authorized, re-run with SQL_WRITE_AUTHORIZED=1." >&2
  exit 2
fi

exit 0

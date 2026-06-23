#!/usr/bin/env bash
# PLACEMENT: .claude/hooks/sql-guard.sh   (chmod +x after creating)
# PURPOSE: PreToolUse hook for Bash. Blocks destructive SQL ONLY when it is
#          actually routed through a known database CLI, so client/production
#          databases stay read-only by default (Constitution Article 2).
#          Exit 2 = BLOCK. Exit 0 = allow.
#
# Design (for Sergio):
#   The guard blocks only when BOTH conditions hold at the same time:
#     (a) the command invokes a known database tool (sqlcmd, psql, ...), AND
#     (b) the command contains a destructive SQL verb (DROP, DELETE, ...).
#   If either is missing, the command is allowed. This removes the false
#   positives of the old "any destructive word anywhere" rule, so things like
#   "git merge", "update the docs" or deleting a temp file no longer trip it.
#
#   TRADE-OFF (read this): being precise makes the guard MORE PERMISSIVE.
#   Destructive SQL sent through a path that is NOT in the tool list below is
#   invisible to this guard — e.g. a Python/Node script that opens its own DB
#   connection, an ORM, an MCP write, or a DB CLI not yet listed. Treat this
#   hook as a guard-rail for the common CLIs, not a complete DB firewall.
#   Defence in depth: pair it with a read-only DB account and a read-only MCP.
#
#   To AUTHORIZE a specific write: set SQL_WRITE_AUTHORIZED=1 for the session.

set -euo pipefail

# Escape hatch: explicit, per-session authorization (unchanged).
if [[ "${SQL_WRITE_AUTHORIZED:-0}" == "1" ]]; then
  exit 0
fi

payload="$(cat)"

# Extract the Bash command. jq is preferred; fall back to the raw payload.
if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"
else
  cmd="$payload"
fi

# (a) Known database CLIs. Whole-word matched, so "psql" will not match
#     "psqlrc" and "mysql" will not match "mysqldump".
#     TO ADD A TOOL: append its executable name to this alternation, e.g.
#     ...|sqlite3|cockroach|clickhouse-client|bcp).
db_tools='(^|[^A-Za-z0-9_])(sqlcmd|psql|mysql|mariadb|mongosh|sqlite3)([^A-Za-z0-9_]|$)'

# (b) Destructive SQL verbs (whole-word; "updated_at" does not trip "UPDATE").
destructive='(^|[^A-Za-z_])(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|EXEC|EXECUTE|GRANT|REVOKE|MERGE)([^A-Za-z_]|$)'

# Block ONLY when a database tool AND a destructive verb are both present.
if printf '%s' "$cmd" | grep -Eiq "$db_tools"; then
  if printf '%s' "$cmd" | grep -Eiq "$destructive"; then
    echo "BLOCKED by sql-guard.sh: destructive SQL routed through a database tool." >&2
    echo "Production data is read-only by default (Constitution Article 2)." >&2
    echo "If this write is authorized, re-run with SQL_WRITE_AUTHORIZED=1." >&2
    exit 2
  fi
fi

exit 0

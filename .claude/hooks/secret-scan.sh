#!/usr/bin/env bash
# PLACEMENT: .claude/hooks/secret-scan.sh   (chmod +x after creating)
# PURPOSE: PreToolUse hook for Edit|Write. Blocks writing common secret patterns.
# CONTRACT: Claude Code passes the tool call as JSON on stdin. We inspect the
#           text being written. Exit 2 = BLOCK the tool call. Exit 0 = allow.
#
# Learning note (for Sergio):
#   - Hooks receive a JSON payload on stdin describing the tool call.
#   - tool_input.content (Write) or tool_input.new_string (Edit) holds the text.
#   - `exit 2` is the magic number: it tells Claude Code to deny the action and
#     feed stderr back to the model so it knows why it was blocked.

set -euo pipefail

payload="$(cat)"

# Extract the text being written, whether it's a Write (content) or Edit (new_string).
# jq is preferred; fall back to grep if jq is unavailable.
if command -v jq >/dev/null 2>&1; then
  text="$(printf '%s' "$payload" | jq -r '.tool_input.content // .tool_input.new_string // ""')"
else
  text="$payload"
fi

# Secret patterns: Anthropic keys, GitHub tokens, generic API keys, and
# SQL Server / Postgres connection strings with embedded credentials.
patterns=(
  'sk-[A-Za-z0-9]{16,}'
  'ghp_[A-Za-z0-9]{20,}'
  'AKIA[0-9A-Z]{16}'
  'password\s*=\s*[^;[:space:]]+'
  'pwd\s*=\s*[^;[:space:]]+'
  'connectionstring\s*=\s*.+'
  '(api[_-]?key|secret|token)\s*[:=]\s*["'"'"'][^"'"'"']{8,}'
)

for p in "${patterns[@]}"; do
  if printf '%s' "$text" | grep -Eiq "$p"; then
    echo "BLOCKED by secret-scan.sh: content matches a secret pattern ($p)." >&2
    echo "Use an environment variable or a secrets manager instead." >&2
    exit 2
  fi
done

exit 0

# PMR Corrections Module — Migration Plan (React → Streamlit)

## Prerequisite (environment)
- **Python is not installed locally** (only the Microsoft Store alias stubs exist on PATH).
  To run/build, install Python 3.11+ **or** containerize with Docker (as the Shelly project
  does). The ported rules engine and tests are written but **could not be executed locally**
  until a real Python interpreter is available.

## Phase 0 — Port the rules engine ✅ (done, UI-agnostic, framework-safe)
- `src/rules_engine.py` — faithful Python port of the React `getValidationErrors`
  (operators, conditions, static/field values, date compare). Pure Python; no UI imports,
  so it survives any UI choice (Streamlit / Dash / Reflex).
- `tests/test_rules_engine.py` — asserts behavior against real `initialRules`.
- **Findings to confirm with Sergio:**
  1. JS-fidelity quirk: `isEmpty` treats numeric `0` and boolean `False` as "empty".
     Confirm this is acceptable, or fix during the port.
  2. Rule 8 in the source (`currentPremium >= expiringPremium` flagged as broken) appears
     **inverted** vs. its message ("must be ≥"). Likely a misconfigured rule — confirm.

## Phase 1 — Decisions (BLOCKED on the analysis/architecture doc)
Drop the doc in `docs/architecture/`. It must resolve:
- Audience (internal vs customer-facing), data home (DB), rich editable grid (must-have?),
  auth (SSO?), expected concurrency. See `docs/adr/0001-...` decision drivers.

## Phase 2 — Data + backend
- Define the policy schema and persistence (DB). Port `generateDummyPolicies` to pandas for
  dev/seed data. Add the change/audit log table. Real authentication.

## Phase 3 — Streamlit app (by modules)
- Tabs: Price Monitor Report · Policy Workbench · Governance Center · Configuration.
- Map: tables → `st.dataframe`; edit → `st.dialog`; bulk import → `st.file_uploader`+pandas;
  export → `st.download_button`. Rich grid → `streamlit-aggrid` only if confirmed.

## Phase 4 — Auth, roles, country scoping; QA (`qa-engineer`); security review (`security-auditor`).

> Project agent: `.claude/agents/streamlit-migrator.md`. Build phase by phase, verifying by
> running the app.

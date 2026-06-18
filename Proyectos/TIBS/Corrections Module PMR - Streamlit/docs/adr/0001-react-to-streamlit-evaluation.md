# ADR-0001: Evaluate re-platforming the React app to Streamlit

| Field    | Value                          |
|----------|--------------------------------|
| Status   | Draft — code analyzed; Streamlit assessed as a strong fit. Pending product context (audience + backend strategy). |
| Date     | 2026-06-18                     |
| Source   | chubb_policy_validation_system_v54_clearer_rule_ui.tsx (1888 lines, single-file React + Tailwind, SheetJS via window.XLSX) |
| Deciders | Sergio Tortolero, Claude       |
| Project  | Corrections Module PMR - Streamlit |

## Context
Sergio wants to move an existing React app to **Streamlit**. This is a **re-platform**,
not a refactor: it changes language (JS/TS → Python), execution model (browser SPA →
server script that re-runs on each interaction), and UI paradigm (React components →
Streamlit widgets). The goal of this ADR is to decide *whether* and *how*, and to list
alternatives that fulfill the React app's functionality.

## Paradigm differences (why this is not a 1:1 port)
| Aspect            | React                                   | Streamlit                                         |
|-------------------|-----------------------------------------|---------------------------------------------------|
| Language          | JavaScript / TypeScript                 | Python                                            |
| Execution         | Client-side SPA, virtual DOM            | Server re-runs the whole script top-to-bottom per interaction (cached) |
| UI model          | Components + hooks, full control        | Prebuilt widgets, opinionated layout              |
| State             | useState/useReducer/Redux               | `st.session_state` (coarser, simpler)             |
| Styling           | Full CSS/any design system              | Limited theming; custom UI needs Streamlit Components (React under the hood) |
| Routing           | Full client routing                     | Multipage apps (no deep client routing)           |
| Real-time/mobile  | Websockets, responsive, PWA             | Limited; not a mobile-first tool                  |
| SEO               | SSR/SSG possible                        | Not suitable (server app behind login typically)  |
| Deployment        | Static/Vercel/Node                      | Python server (Streamlit Community Cloud / container) |

## What transfers vs. what is at risk
**Transfers well**
- Business logic (rewritten in Python) — especially data processing, calculations, ML.
- Calls to an existing backend/API (Streamlit just calls the same endpoints).
- Tables, forms, charts, dashboards, file upload/download, simple wizards.

**At risk / costly**
- Highly custom or branded UI, animations, complex/fine-grained interactions.
- Client-side routing and deep-linking.
- High-concurrency public traffic (each user is a server session).
- Anything depending on the npm React ecosystem.

## Alternatives to fulfill the React app's functionality
1. **Streamlit** — fastest for data apps / internal tools / ML demos; weakest for custom UX and scale.
2. **Reflex** (formerly Pynecone) — write pure Python, compiles to a **React** app. Best
   bridge if the goal is "Python team" but you still need React-grade UI/UX.
3. **Dash (Plotly)** — more layout/control than Streamlit; strong for enterprise dashboards.
4. **Gradio** — ideal specifically for ML/AI model demos and quick interfaces.
5. **NiceGUI / Shiny for Python / Panel** — other Python UI options with different trade-offs.
6. **Keep React, simplify** — if the real goal is less maintenance, not Python.
7. **Hybrid** — Streamlit/Gradio for the data/ML parts; keep React for the customer-facing parts.
8. **Streamlit + Custom Components** — embed React widgets inside Streamlit for the few
   screens that truly need custom UI.

## Decision drivers (to be filled with Sergio's answers)
- **Audience:** customer-facing product vs. internal/data tool. (Streamlit shines for internal.)
- **UI complexity:** mostly forms/tables/charts vs. bespoke branded UX.
- **Team & motivation:** Python-first team? data/ML heavy? maintenance reduction?
- **Architecture:** logic in a backend API (portable) vs. all in the React frontend (rewrite).
- **Scale:** expected concurrent users and performance needs.

## Specific analysis — "PMR Corrections Module" (Chubb LATAM)
An internal insurance tool to review/correct policy data for the Price Monitor Report.
Single-file React app, **no backend** (1000 policies generated in-browser, state resets on
refresh). Modules:
- **Auth & roles** — login, 4 users, roles (Admin / Actuary / Underwriter), country scoping
  (Underwriters see only their country), user switching. Hardcoded, no real auth.
- **Price Monitor Report** — KPIs (premium renewed/expiring, % change), Bound-policy table.
- **Policy Workbench** — filters, clickable cross-filtering KPI cards, sortable/paginated
  table (1000 rows), per-policy edit modal, bulk edit, bulk import (CSV/XLSX with column-
  mapping wizard), export to Excel.
- **Governance Center** — read-only change log / audit of modified policies.
- **Configuration (Admin)** — full **validation-rules engine** CRUD (target + operator +
  static-or-field value + optional AND conditions + conflict detection), correction
  deadline, high-value threshold.
- **Cross-cutting** — change/audit trail (user, role, timestamp, from→to), toasts, modals,
  tooltips, pagination, sorting, multi-select.

### Feature-by-feature mapping to Streamlit
| Feature | Streamlit equivalent | Effort / fidelity |
|---|---|---|
| Tabs / navigation | `st.tabs` or multipage `st.navigation` | Easy / high |
| Tables (sort, paginate) | `st.dataframe` (built-in sort) | Easy / high |
| Filters panel | sidebar widgets + `st.columns` | Easy / high |
| KPI cards | `st.metric` in `st.columns` | Easy / medium (clickable cross-filter via buttons + `session_state`) |
| Export to Excel | `st.download_button` + pandas/openpyxl | Easy / high (better than SheetJS) |
| Bulk import + mapping wizard | `st.file_uploader` + pandas + `session_state` steps | Medium / high |
| **Validation rules engine** | pure Python port of `getValidationErrors` + rule schema | Easy / high (near 1:1) |
| Dummy data (1000) | pandas/numpy + `st.cache_data` | Easy / high |
| Per-policy edit modal | `st.dialog` + form | Medium / medium |
| Inline cell change-highlight, strike-through old value, "last changed by" tooltips | `st.column_config` styling (limited) | Hard / **low — fidelity loss** |
| Rule editor (dynamic conditions, field-vs-static toggle, conflict check) | `session_state`-driven form | Medium-Hard / medium (works; dynamic add/remove clunkier under rerun) |
| Roles + country scoping | `session_state` gating | Medium / high |
| Auth / login | `st.login` (OIDC) or `streamlit-authenticator` | Medium (must add) |
| Branding (Chubb colors, Tailwind) | theme + limited custom CSS | Medium / low-medium |
| **Persistence of edits / audit log** | **needs a database** (none today) | — must add |

### Assessment
For **this** app Streamlit is a **strong, arguably excellent fit**: ~60–70% of the React
code is UI plumbing (modals, tables, pagination, tooltips) that Streamlit replaces with
built-ins, and the business logic (rules engine, validation, Excel I/O) is cleanly
separable and ports almost 1:1 to Python + pandas. It is an internal, tabular, form-and-
validation tool — squarely Streamlit's sweet spot.

**Real losses / risks:**
1. Rich inline-edit table UX (per-cell highlight, strike-through, field tooltips) — degraded.
2. Pixel-perfect Chubb branding — limited.
3. The rule editor's dynamic UX — functional but less fluid under Streamlit's rerun model.

**The biggest hidden work is not the UI — it is that there is no backend.** Today the app
is a front-end prototype with random data that resets on refresh. To make it real (any
path) you need: a **database** (persist policies, edits, audit log) and **real auth**.
This is exactly where the workspace's `Tablero de Consolidación Financiera` thread could converge — the policy
data likely lives in the same SQL/Power BI ecosystem.

## Decision (recommendation, to confirm with product context)
- **If this stays an internal underwriting tool (most likely):** go **Streamlit** for the
  app layer + add a **SQL backend** for persistence. Fastest path to a usable, maintainable
  internal product; accept minor UX-polish losses.
- **If the rich editable-grid UX is a hard requirement:** use **Streamlit + `streamlit-aggrid`**,
  or consider **Dash + dash-ag-grid** (AG Grid gives the React-grade editable table).
- **If it will become broker/customer-facing or branding-critical:** keep/rebuild in
  **React** (with a real backend), or use **Reflex** (Python → React) to keep Python skills.

## Open questions (to finalize the decision)
- [ ] Audience: internal underwriters only, or broker/customer-facing?
- [ ] Where should the data live (SQL Server / Azure SQL — same as the Tablero de Consolidación Financiera project)?
- [ ] Is the rich inline-edit table UX a must-have, or is a standard editable grid acceptable?
- [ ] Auth: integrate with corporate SSO (Azure AD/Entra) or app-level login?
- [ ] Expected concurrent users (sizing)?

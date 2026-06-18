"""Validation rules engine for the PMR Corrections Module.

Phase 0 of the React -> Streamlit re-platform: a faithful, **UI-agnostic** port of the
React `getValidationErrors` logic (from `chubb_policy_validation_system_v54...tsx`).

This module is pure Python (no Streamlit/UI imports), so it is reusable regardless of the
final UI framework (Streamlit, Dash, Reflex). It mirrors the original JavaScript semantics
on purpose — including JS-style "falsy" emptiness and parseFloat-style numeric coercion —
so behavior matches the current app exactly. Quirks worth reviewing are flagged with
`NOTE (fidelity)`.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Sequence

Policy = Mapping[str, Any]
Rule = Mapping[str, Any]


# --- coercion helpers (mirror JS) -------------------------------------------------

def _parse_float(value: Any) -> float:
    """Mirror JS ``parseFloat``: return a float, or NaN if not parseable.

    Any comparison against NaN is False, exactly like JS.
    """
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return float("nan")


def _to_num(value: Any):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def _is_empty(value: Any) -> bool:
    """Mirror JS ``!value || String(value).trim() === ''``.

    NOTE (fidelity): JS treats ``0`` and ``False`` as empty (because ``!0`` is true).
    Python's ``not value`` reproduces this. Flag this with Sergio if a numeric ``0`` or a
    boolean ``False`` should NOT count as "empty".
    """
    return (not value) or str(value).strip() == ""


def _loose_eq(a: Any, b: Any) -> bool:
    """Approximate JS loose equality (``==``) for the value types used by the rules."""
    if a is None and b is None:
        return True
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b)
    na, nb = _to_num(a), _to_num(b)
    if na is not None and nb is not None:
        return na == nb
    return str(a) == str(b)


def _resolve_value(policy: Policy, value_type: str, value: Any) -> Any:
    """Static value, or the value of another policy field when value_type == 'field'."""
    if value_type == "field":
        return policy.get(value)
    # static: coerce the JS string booleans, like the React code does for conditions
    if value == "true":
        return True
    if value == "false":
        return False
    return value


# --- condition + target evaluation ------------------------------------------------

def _condition_met(policy: Policy, cond: Mapping[str, Any]) -> bool:
    policy_value = policy.get(cond["field"])
    comparison = _resolve_value(policy, cond.get("valueType", "static"), cond.get("value"))
    op = cond["operator"]

    if op == "equals":
        return _loose_eq(policy_value, comparison)
    if op == "notEquals":
        return not _loose_eq(policy_value, comparison)
    if op == "greaterThan":
        return _parse_float(policy_value) > _parse_float(comparison)
    if op == "lessThan":
        return _parse_float(policy_value) < _parse_float(comparison)
    if op == "greaterThanOrEqual":
        return _parse_float(policy_value) >= _parse_float(comparison)
    if op == "lessThanOrEqual":
        return _parse_float(policy_value) <= _parse_float(comparison)
    if op == "isNotNull":
        return policy_value is not None and policy_value != ""
    if op == "isEmpty":
        return _is_empty(policy_value)
    if op == "contains":
        return str(comparison) in str(policy_value)
    if op == "notContains":
        return str(comparison) not in str(policy_value)
    return True  # unknown operator -> condition passes (mirrors JS default)


def _target_broken(policy: Policy, target: Mapping[str, Any]) -> bool:
    policy_value = policy.get(target["field"])
    target_value = (
        policy.get(target["value"]) if target.get("valueType") == "field" else target.get("value")
    )
    op = target["operator"]

    if op == "isEmpty":
        return _is_empty(policy_value)
    if op in ("isBefore", "isAfter"):
        if policy_value and target_value:
            d1 = _to_date(policy_value)
            d2 = _to_date(target_value)
            if d1 is None or d2 is None:
                return False
            if op == "isBefore":
                return d1 >= d2  # broken when NOT before
            return d1 <= d2       # broken when NOT after
        return False
    if op == "lessThan":
        return _parse_float(policy_value) < _parse_float(target_value)
    if op == "greaterThan":
        return _parse_float(policy_value) > _parse_float(target_value)
    if op == "lessThanOrEqual":
        return _parse_float(policy_value) <= _parse_float(target_value)
    if op == "greaterThanOrEqual":
        return _parse_float(policy_value) >= _parse_float(target_value)
    return False


def _to_date(value: Any):
    if isinstance(value, datetime):
        return value
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(str(value), fmt)
        except (TypeError, ValueError):
            continue
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


# --- public API -------------------------------------------------------------------

def get_validation_errors(policy: Policy, rules: Sequence[Rule]) -> dict[str, str]:
    """Return {field: message} for every active, applicable rule the policy breaks.

    Faithful port of the React `getValidationErrors`. If multiple rules target the same
    field, the last one wins (same as the JS object-assignment behavior).
    """
    errors: dict[str, str] = {}
    if not policy:
        return errors
    for rule in rules:
        if not rule.get("isActive", True):
            continue
        if all(_condition_met(policy, c) for c in rule.get("conditions", [])):
            if _target_broken(policy, rule["target"]):
                errors[rule["target"]["field"]] = rule["message"]
    return errors

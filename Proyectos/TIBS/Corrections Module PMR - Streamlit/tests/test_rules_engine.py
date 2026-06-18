"""Tests for the ported validation rules engine.

Run: `python tests/test_rules_engine.py`  (no external deps; plain asserts).
Uses a subset of the app's real `initialRules` to confirm fidelity to the React logic.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rules_engine import get_validation_errors  # noqa: E402

# A subset of the React `initialRules`, ported 1:1.
RULES = [
    {  # 1
        "target": {"field": "commentOnValidatedRateChange", "operator": "isEmpty", "valueType": "static", "value": ""},
        "message": "Comment is required when there is a rate change.",
        "isActive": True,
        "conditions": [{"field": "netValidatedRateChange", "operator": "isNotNull", "valueType": "static", "value": ""}],
    },
    {  # 4
        "target": {"field": "expirationDate", "operator": "isAfter", "valueType": "field", "value": "inceptionDate"},
        "message": "Expiration Date must be after Inception Date.",
        "isActive": True,
        "conditions": [],
    },
    {  # 5
        "target": {"field": "netValidatedRateChange", "operator": "isEmpty", "valueType": "static", "value": ""},
        "message": "Net Validated Rate Change is required for Bound policies.",
        "isActive": True,
        "conditions": [{"field": "policyStatus", "operator": "equals", "valueType": "static", "value": "Bound"}],
    },
    {  # 7
        "target": {"field": "adequacyPERC", "operator": "lessThan", "valueType": "static", "value": 95},
        "message": "Adequacy PERC for Fire LOB must be >= 95%.",
        "isActive": True,
        "conditions": [{"field": "lob", "operator": "equals", "valueType": "static", "value": "Fire"}],
    },
]


def _check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    assert condition, name


def run():
    # Rule 5: Bound policy with empty rate change -> error.
    p = {"policyStatus": "Bound", "netValidatedRateChange": None}
    errs = get_validation_errors(p, RULES)
    _check("Bound + empty netValidatedRateChange flags rule 5",
           errs.get("netValidatedRateChange") == "Net Validated Rate Change is required for Bound policies.")

    # Rule 5: non-Bound policy is NOT flagged (condition not met).
    p = {"policyStatus": "Quoted", "netValidatedRateChange": None}
    _check("Non-Bound policy is not flagged by rule 5",
           "netValidatedRateChange" not in get_validation_errors(p, RULES))

    # Rule 7: Fire policy with adequacy 90 (<95) -> error.
    p = {"lob": "Fire", "adequacyPERC": 90}
    _check("Fire + adequacy 90 flags rule 7",
           get_validation_errors(p, RULES).get("adequacyPERC") == "Adequacy PERC for Fire LOB must be >= 95%.")

    # Rule 7: Fire policy with adequacy 96 -> OK.
    p = {"lob": "Fire", "adequacyPERC": 96}
    _check("Fire + adequacy 96 is OK", "adequacyPERC" not in get_validation_errors(p, RULES))

    # Rule 1: rate change present but no comment -> error.
    p = {"netValidatedRateChange": 0.05, "commentOnValidatedRateChange": ""}
    _check("Rate change + empty comment flags rule 1",
           "commentOnValidatedRateChange" in get_validation_errors(p, RULES))

    # Rule 4: expiration before inception -> error (must be after).
    p = {"inceptionDate": "2024-06-01", "expirationDate": "2024-01-01"}
    _check("Expiration before inception flags rule 4",
           "expirationDate" in get_validation_errors(p, RULES))

    # Rule 4: expiration after inception -> OK.
    p = {"inceptionDate": "2024-01-01", "expirationDate": "2024-06-01"}
    _check("Expiration after inception is OK", "expirationDate" not in get_validation_errors(p, RULES))

    print("\nAll assertions passed.")


if __name__ == "__main__":
    run()

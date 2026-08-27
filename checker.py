def check_diagnosis(ai_result, row):
    """
    Deterministic validation of an AI diagnosis.

    Checks:
    1. Whether the AI root cause matches the expected fault.
    2. Whether the AI diagnosis references supplied evidence.
    """

    expected = str(row["expected_fault"]).lower().strip()
    root = str(ai_result.get("root_cause", "")).lower().strip()

    root_ok = expected in root or root in expected

    evidence_text = " ".join(
        str(x) for x in ai_result.get("evidence", [])
    ).lower()

    show_outputs = str(row["show_outputs"]).lower()

    evidence_ok = False

    for token in show_outputs.split():
        token = token.strip(".,:;()[]{}")

        if len(token) >= 4 and token in evidence_text:
            evidence_ok = True
            break

    return {
        "root_cause_match": root_ok,
        "evidence_referenced": evidence_ok,
        "overall": root_ok and evidence_ok,
    }
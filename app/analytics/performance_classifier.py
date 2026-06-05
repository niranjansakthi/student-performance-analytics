"""
Performance classification module.

Classifies students into performance tiers based on a holistic
evaluation of CGPA, internal marks, exam scores, backlogs, and
assignment completion.

Tiers:
    EXCELLENT  — outstanding across all academic dimensions
    GOOD       — solid performance with minor gaps
    AVERAGE    — meets minimum expectations
    AT RISK    — below expectations; needs intervention
"""


def classify_performance(
    cgpa: float,
    internal_marks: int | None = None,
    exam_score: int | None = None,
    backlogs_count: int = 0,
    assignments_completed: int = 0,
) -> str:
    """
    Return one of: 'EXCELLENT', 'GOOD', 'AVERAGE', 'AT RISK'.

    The classification follows a top-down evaluation:
    any disqualifying factor pushes the student to a lower tier.
    """

    # ── Immediate AT RISK triggers ────────────────────────────────────────────
    if backlogs_count >= 3:
        return "AT RISK"

    if cgpa < 4.5:
        return "AT RISK"

    # ── EXCELLENT tier ────────────────────────────────────────────────────────
    is_excellent = (
        cgpa >= 8.5
        and backlogs_count == 0
        and assignments_completed >= 15
    )

    if internal_marks is not None:
        is_excellent = is_excellent and internal_marks >= 75

    if exam_score is not None:
        is_excellent = is_excellent and exam_score >= 75

    if is_excellent:
        return "EXCELLENT"

    # ── GOOD tier ─────────────────────────────────────────────────────────────
    is_good = (
        cgpa >= 6.5
        and backlogs_count <= 1
        and assignments_completed >= 10
    )

    if internal_marks is not None:
        is_good = is_good and internal_marks >= 50

    if exam_score is not None:
        is_good = is_good and exam_score >= 50

    if is_good:
        return "GOOD"

    # ── AVERAGE vs AT RISK ────────────────────────────────────────────────────
    if cgpa >= 5.0 and backlogs_count <= 2:
        return "AVERAGE"

    return "AT RISK"

"""
Risk score calculation and classification.

The risk score is a weighted composite (0–100) that identifies students
who may be at academic risk. Higher score = higher risk.

Weight distribution:
    Attendance       — 25 pts max
    CGPA             — 25 pts max
    Backlogs         — 20 pts max
    Internal Marks   — 10 pts max
    Exam Score       — 10 pts max
    Library Visits   —  5 pts max
    Assignments      —  5 pts max
"""


def calculate_risk_score(
    attendance: float,
    cgpa: float,
    library_visits: int,
    assignments_completed: int,
    backlogs_count: int = 0,
    internal_marks: int | None = None,
    exam_score: int | None = None,
) -> int:
    """Return an integer risk score between 0 and 100."""

    risk_score = 0

    # ── Attendance risk (25 pts) ──────────────────────────────────────────────
    if attendance < 65:
        risk_score += 25
    elif attendance < 75:
        risk_score += 18
    elif attendance < 85:
        risk_score += 8

    # ── CGPA risk (25 pts) ────────────────────────────────────────────────────
    if cgpa < 4.0:
        risk_score += 25
    elif cgpa < 5.0:
        risk_score += 20
    elif cgpa < 6.0:
        risk_score += 12
    elif cgpa < 7.0:
        risk_score += 5

    # ── Backlogs risk (20 pts) ────────────────────────────────────────────────
    if backlogs_count >= 4:
        risk_score += 20
    elif backlogs_count >= 3:
        risk_score += 15
    elif backlogs_count >= 2:
        risk_score += 10
    elif backlogs_count >= 1:
        risk_score += 5

    # ── Internal marks risk (10 pts) ──────────────────────────────────────────
    if internal_marks is not None:
        if internal_marks < 35:
            risk_score += 10
        elif internal_marks < 50:
            risk_score += 6
        elif internal_marks < 60:
            risk_score += 3

    # ── Exam score risk (10 pts) ──────────────────────────────────────────────
    if exam_score is not None:
        if exam_score < 35:
            risk_score += 10
        elif exam_score < 50:
            risk_score += 6
        elif exam_score < 60:
            risk_score += 3

    # ── Engagement risk (5 + 5 = 10 pts) ──────────────────────────────────────
    if library_visits < 3:
        risk_score += 5
    elif library_visits < 5:
        risk_score += 2

    if assignments_completed < 5:
        risk_score += 5
    elif assignments_completed < 8:
        risk_score += 2

    return min(risk_score, 100)


def classify_risk(risk_score: int) -> str:
    """Classify a risk score into HIGH / MEDIUM / LOW."""

    if risk_score >= 60:
        return "HIGH"
    elif risk_score >= 35:
        return "MEDIUM"
    return "LOW"
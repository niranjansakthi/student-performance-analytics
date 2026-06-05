"""
Engagement score calculation.

The engagement score measures how actively a student participates in
academic and co-curricular activities. Higher score = more engaged.

Formula:
    attendance * 0.4
    + library_visits * 2
    + assignments_completed * 3
    + workshop_attendance * 2.5
"""


def calculate_engagement_score(
    attendance: float,
    library_visits: int,
    assignments_completed: int,
    workshop_attendance: int = 0,
) -> float:
    """Return a numeric engagement score (not bounded)."""

    score = (
        attendance * 0.4
        + library_visits * 2
        + assignments_completed * 3
        + workshop_attendance * 2.5
    )

    return round(score, 2)
"""add_analytics_columns

Revision ID: 2548fc0eccb9
Revises: 40f76c346396
Create Date: 2026-06-04 17:36:01.089561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2548fc0eccb9'
down_revision: Union[str, Sequence[str], None] = '40f76c346396'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add analytics columns: internal_marks, exam_score, backlogs_count, workshop_attendance."""
    op.add_column(
        'students',
        sa.Column('internal_marks', sa.Integer(), nullable=True,
                  comment='Internal / coursework marks (typically 0–100)'),
    )
    op.add_column(
        'students',
        sa.Column('exam_score', sa.Integer(), nullable=True,
                  comment='Final exam score (typically 0–100)'),
    )
    op.add_column(
        'students',
        sa.Column('backlogs_count', sa.Integer(), nullable=True,
                  server_default='0',
                  comment='Number of active backlogs / failed subjects'),
    )
    op.add_column(
        'students',
        sa.Column('workshop_attendance', sa.Integer(), nullable=True,
                  server_default='0',
                  comment='Number of workshops attended'),
    )


def downgrade() -> None:
    """Remove analytics columns."""
    op.drop_column('students', 'workshop_attendance')
    op.drop_column('students', 'backlogs_count')
    op.drop_column('students', 'exam_score')
    op.drop_column('students', 'internal_marks')

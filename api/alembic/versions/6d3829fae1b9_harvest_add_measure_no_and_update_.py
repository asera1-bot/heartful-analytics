"""harvest add measure_no and update unique constraint

Revision ID: 6d3829fae1b9
Revision: 919cf4dd1785
Create Date: 2026-01-20 10:09:41.110672
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d3829fae1b9'
down_revision: Union[str, None] = '919cf4dd1785'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        UPDATE harvest
        SET measured_at = (month || '-01T00:00:00+00')::timestamptz
        WHERE measured_at IS NULL;
    """)

    op.alter_column("harvest", "measured_at", nullable=False)

    op.add_column(
        "harvest",
        sa.Column("measure_no", sa.Integer(), nullable=False, server_default="1"),
    )

    op.alter_column("harvest", "measure_no", server_default=None)

    op.execute("""
        ALTER TABLE harvest
        DROP CONSTRAINT IF EXISTS uq_harvest_month_company_crop;
    """)

    op.create_unique_constraint(
        "uq_harvest_company_crop_measured_at_no",
        "harvest",
        ["company", "crop", "measured_at", "measure_no"],
    )

def downgrade() -> None:
    op.drop_constraint(
        "uq_harvest_company_crop_measured_at_no",
        "harvest",
        type_="unique",
    )

    op.drop_column("harvest", "measure_no")

    op.alter_column("harvest", "measured_at", nullable=True)

    op.create_unique_constraint(
        "uq_harvest_month_company_crop",
        "harvest",
        ["month", "company", "crop"],
    )


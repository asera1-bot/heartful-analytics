"""add unique constraint to harvest (month, company, crop)

Revision ID: a66a47f3285e
Revision: 654b14bb721d
Create Date: 2026-01-18 06:02:20.073111
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a66a47f3285e'
down_revision: Union[str, None] = '654b14bb721d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_unique_constraint(
            "uq_harvest_month_company_crop",
            "harvest",
            ["month", "company", "crop"],
    )

def downgrade() -> None:
    op.drop_constraint("uq_harvest_month_company_crop", "harvest", type="unique")


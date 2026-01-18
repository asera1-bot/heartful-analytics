"""fix uq_env_month_medium

Revision ID: 654b14bb721d
Revision: 14df3cb5467c
Create Date: 2026-01-18 04:12:15.261609
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654b14bb721d'
down_revision: Union[str, None] = '14df3cb5467c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    #op.create_unique_constraint(
    #        "uq_env_month_medium",
    #        "env",
    #        ["month", "medium"],
    #)
    pass

def downgrade() -> None:
    #op.drop_constraint("uq_env_month_medium,", "env", type="unique")
    pass

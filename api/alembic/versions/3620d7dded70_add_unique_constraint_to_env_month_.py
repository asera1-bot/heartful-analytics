"""add unique constraint to env (month, medium)

Revision ID: 3620d7dded70
Revision: 8df0522dd904
Create Date: 2026-01-17 07:12:20.401587
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3620d7dded70'
down_revision: Union[str, None] = '8df0522dd904'
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
    #op.drop_constraint("uq_env_month_medium", "env", type="unique")
    pass

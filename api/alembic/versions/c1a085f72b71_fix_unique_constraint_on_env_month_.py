"""fix unique constraint on env (month, medium)

Revision ID: c1a085f72b71
Revision: 3620d7dded70
Create Date: 2026-01-17 07:37:25.113065
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a085f72b71'
down_revision: Union[str, None] = '3620d7dded70'
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
    #op.drop_constraint(
    #    "uq_env_month_medium",
    #    "env",
    #    type_="unique",
    #)
    pass

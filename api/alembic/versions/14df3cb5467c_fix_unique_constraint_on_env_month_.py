"""fix unique constraint on env (month, medium)

Revision ID: 14df3cb5467c
Revision: c1a085f72b71
Create Date: 2026-01-17 07:42:49.194692
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14df3cb5467c'
down_revision: Union[str, None] = 'c1a085f72b71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass


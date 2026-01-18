"""add measured_at to harvest

Revision ID: 919cf4dd1785
Revision: a66a47f3285e
Create Date: 2026-01-18 07:31:50.831859
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '919cf4dd1785'
down_revision: Union[str, None] = 'a66a47f3285e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # measured_at　を　nullable=True　で追加
    op.add_column(
            "harvest",
            sa.Column("measured_at", sa.DateTime(timezone=True), nullable=True),
    )

def downgrade() -> None:
    # month が 'YYYY-MM' なので 'YYYY-MM-01T00:00:00+00' を作る側
    op.execute("""
        UPDATE harvest
        SET measured_at = (month || '-01T00:00:00+00')::timestaptz
        WHERE measured_at IS NULL;
    """)

    # NOT NULL にする
    op.alter_column("harvest", "measured_at", nullable=False)

    # 旧ユニーク制約を落とす（存在しない可能性もあるのでIF EXISTS 相当の工夫）
    #Alembic にはIF EXISTS　がないのでSQLで落とすのが安全
    op.execute("""
        ALTER TABLE harvest
        DROP CONSTRAINT IF EXISTS uq_harvest_month_company_crop;
    """)

    # 新ユニーク制約
    op.create_unique_constraint(
            "uq_harvest_measured_company_crop",
            "harvest",
            ["measured_at", "company", "corp"],
    )

def downgrade() -> None:
    op.drop_constraint("uq_harvest_measured_company_crop", "harvest", type_="unique")
    op.drop_column("harvest", "measured_at")
    # 旧制約は必要なら戻す
    op.create_unique_constraint(
            "uq_harvest_month_company_crop",
            "harvest",
            ["month", "company", "crop"],
    )

"""change amount to float

Revision ID: d44e00fcc12d
Revises: 4e2a81f0a7fe
Create Date: 2026-05-04 21:24:24.135639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd44e00fcc12d'
down_revision: Union[str, Sequence[str], None] = '4e2a81f0a7fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "approval_requests",
        "amount",
        existing_type=sa.Integer,
        type_=sa.Float,
        existing_nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "approval_requests",
        "amount",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=True
    )
"""Create phone number for user column

Revision ID: ee8f07b2b068
Revises: 
Create Date: 2024-11-27 14:27:43.399773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee8f07b2b068'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column("phone_number",sa.String(),nullable=True))


def downgrade() -> None:
    pass

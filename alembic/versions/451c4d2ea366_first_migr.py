"""first migr

Revision ID: 451c4d2ea366
Revises: 47ba6f2499dd
Create Date: 2024-03-27 09:07:07.525634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '451c4d2ea366'
down_revision: Union[str, None] = '47ba6f2499dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('contact1', sa.String(), nullable=True))
    op.alter_column('users', 'contact2',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'contact2',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'contact1')
    # ### end Alembic commands ###
"""Add URLRecord table

Revision ID: 17e6b088e8c3
Revises: 83da404e27d7
Create Date: 2025-02-09 13:05:55.507235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17e6b088e8c3'
down_revision: Union[str, None] = '83da404e27d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_url_records_id'), 'url_records', ['id'], unique=False)
    op.create_index(op.f('ix_url_records_url'), 'url_records', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_records_url'), table_name='url_records')
    op.drop_index(op.f('ix_url_records_id'), table_name='url_records')
    op.drop_table('url_records')
    # ### end Alembic commands ###

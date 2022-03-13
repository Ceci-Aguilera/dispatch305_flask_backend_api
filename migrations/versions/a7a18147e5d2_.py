"""empty message

Revision ID: a7a18147e5d2
Revises: c19bd3185772
Create Date: 2022-03-12 19:14:20.697856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7a18147e5d2'
down_revision = 'c19bd3185772'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useradmin', sa.Column('active', sa.Boolean(), nullable=True))
    op.drop_column('useradmin', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useradmin', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('useradmin', 'active')
    # ### end Alembic commands ###
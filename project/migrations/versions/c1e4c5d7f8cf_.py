"""Created and Updated

Revision ID: c1e4c5d7f8cf
Revises: 7a5206449bdb
Create Date: 2022-09-28 20:04:25.662423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1e4c5d7f8cf'
down_revision = '7a5206449bdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('card', 'updated_on')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('updated_on', sa.DATETIME(), nullable=True))
    op.drop_column('card', 'updated_at')
    # ### end Alembic commands ###
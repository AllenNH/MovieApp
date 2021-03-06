"""added status for show

Revision ID: fafb7a39e7bd
Revises: d4095e97390e
Create Date: 2022-03-24 17:45:31.445101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fafb7a39e7bd'
down_revision = 'd4095e97390e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'status')
    # ### end Alembic commands ###

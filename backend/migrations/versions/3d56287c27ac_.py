"""empty message

Revision ID: 3d56287c27ac
Revises: 88bd52775476
Create Date: 2024-07-03 22:23:06.732992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d56287c27ac'
down_revision = '88bd52775476'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('available_domains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))

    with op.batch_alter_table('domains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zone', sa.String(), nullable=False))

    with op.batch_alter_table('keyword_stats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))

    with op.batch_alter_table('unavailable_domains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unavailable_domains', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    with op.batch_alter_table('keyword_stats', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    with op.batch_alter_table('domains', schema=None) as batch_op:
        batch_op.drop_column('zone')

    with op.batch_alter_table('available_domains', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    # ### end Alembic commands ###
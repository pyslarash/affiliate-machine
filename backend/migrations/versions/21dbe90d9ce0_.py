"""empty message

Revision ID: 21dbe90d9ce0
Revises: b1e5819abe56
Create Date: 2024-05-10 01:04:32.072714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21dbe90d9ce0'
down_revision = 'b1e5819abe56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_envs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.String(), nullable=True))
        batch_op.drop_column('hashed_value')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_envs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_value', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('value')

    # ### end Alembic commands ###
"""returned column

Revision ID: 5185287965af
Revises: a0945fb9ed77
Create Date: 2025-04-13 10:08:30.524907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5185287965af'
down_revision = 'a0945fb9ed77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enrolled', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_column('enrolled')

    # ### end Alembic commands ###

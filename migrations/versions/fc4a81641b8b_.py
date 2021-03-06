"""empty message

Revision ID: fc4a81641b8b
Revises: 970ff308f757
Create Date: 2016-02-26 12:21:01.087535

"""

# revision identifiers, used by Alembic.
revision = 'fc4a81641b8b'
down_revision = '970ff308f757'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('authenticated', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user', sa.Column('password', sa.String(), nullable=True))
    op.drop_column('user', 'id')
    op.drop_column('user', 'name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_column('user', 'password')
    op.drop_column('user', 'email')
    op.drop_column('user', 'authenticated')
    ### end Alembic commands ###

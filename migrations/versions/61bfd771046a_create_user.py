"""create user

Revision ID: 61bfd771046a
Revises: 
Create Date: 2021-07-26 16:47:29.455880

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '61bfd771046a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('body', sa.String(length=140), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###

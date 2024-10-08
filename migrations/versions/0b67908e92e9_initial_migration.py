"""Initial migration.

Revision ID: 0b67908e92e9
Revises: 
Create Date: 2024-09-23 09:32:50.942305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b67908e92e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('isbn',
               existing_type=sa.TEXT(),
               type_=sa.String(length=13),
               existing_nullable=True)
        batch_op.alter_column('cover_image',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['isbn'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('cover_image',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('isbn',
               existing_type=sa.String(length=13),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###

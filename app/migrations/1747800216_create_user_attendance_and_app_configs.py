"""create user attendance and app configs

Revision ID: 1747800216
Revises: 1746692750
Create Date: 2025-05-21 11:03:36.488330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1747800216'
down_revision: Union[str, None] = '1746692750'
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_configurations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field', sa.String(length=255), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_application_configurations'))
    )
    op.create_index(op.f('ix_application_configurations_id'), 'application_configurations', ['id'], unique=False)
    op.create_table('user_attendances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('day_date', sa.Date(), nullable=False),
    sa.Column('clock_in', sa.Time(), nullable=False),
    sa.Column('clock_out', sa.Time(), nullable=True),
    sa.Column('late_in', sa.Boolean(), nullable=False),
    sa.Column('early_out', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_attendances_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_attendances'))
    )
    op.create_index(op.f('ix_user_attendances_id'), 'user_attendances', ['id'], unique=False)
    op.alter_column('user_encrypted_face_embeddings', 'embedding',
               existing_type=mysql.MEDIUMBLOB(),
               type_=sa.LargeBinary(length=1048576),
               existing_nullable=False)
    op.alter_column('user_registered_faces', 'real_content',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=16777216),
               existing_nullable=False)
    op.alter_column('user_registered_faces', 'rgb_content',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=16777216),
               existing_nullable=False)
    op.alter_column('user_tenseal_context', 'context',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=16777216),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_tenseal_context', 'context',
               existing_type=sa.LargeBinary(length=16777216),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('user_registered_faces', 'rgb_content',
               existing_type=sa.LargeBinary(length=16777216),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('user_registered_faces', 'real_content',
               existing_type=sa.LargeBinary(length=16777216),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)
    op.alter_column('user_encrypted_face_embeddings', 'embedding',
               existing_type=sa.LargeBinary(length=1048576),
               type_=mysql.MEDIUMBLOB(),
               existing_nullable=False)
    op.drop_index(op.f('ix_user_attendances_id'), table_name='user_attendances')
    op.drop_table('user_attendances')
    op.drop_index(op.f('ix_application_configurations_id'), table_name='application_configurations')
    op.drop_table('application_configurations')
    # ### end Alembic commands ###

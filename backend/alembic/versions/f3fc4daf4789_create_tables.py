"""create tables

Revision ID: f3fc4daf4789
Revises: 0464b02370cb
Create Date: 2025-03-16 22:35:20.588093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f3fc4daf4789'
down_revision: Union[str, None] = '0464b02370cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('institute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('public_service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('service_type', postgresql.ENUM('k1', 'k2', 'k3', 'q1', 'q2', 'other', name='service_type'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('departament',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('institute_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institute_id'], ['institute.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('public_service_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['public_service_id'], ['public_service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', postgresql.ENUM('assistant', 'teacher', 'department_chair', 'rector_office', name='role'), nullable=True),
    sa.Column('departament_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['departament_id'], ['departament.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', postgresql.ENUM('assistant', 'teacher', 'department_chair', 'rector_office', name='role'), nullable=True),
    sa.Column('departament_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['departament_id'], ['departament.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publication_count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee_metrics')
    op.drop_table('user')
    op.drop_table('report')
    op.drop_table('publication')
    op.drop_table('departament')
    op.drop_table('public_service')
    op.drop_table('institute')
    # ### end Alembic commands ###

"""Initial migrations and user seeding

Revision ID: c59bd683b866
Revises: 
Create Date: 2026-03-18 12:34:19.047725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c59bd683b866'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Create User Table ---
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('role', sa.Enum('ADMIN', 'USER', name='userrole'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)

    # --- Create Item Table ---
    op.create_table(
        'item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_description'), 'item', ['description'], unique=False)
    op.create_index(op.f('ix_item_id'), 'item', ['id'], unique=False)
    op.create_index(op.f('ix_item_title'), 'item', ['title'], unique=False)

    # --- Seed Initial Admin User ---
    # Using passlib locally to hash the password for the migration
    from app.core.security import get_password_hash
    hashed_password = get_password_hash("adminpassword")
    
    op.execute(
        sa.text(
            f"INSERT INTO \"user\" (full_name, email, hashed_password, is_active, role) "
            f"VALUES ('Initial Admin', 'admin@example.com', '{hashed_password}', True, 'ADMIN')"
        )
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_item_title'), table_name='item')
    op.drop_index(op.f('ix_item_id'), table_name='item')
    op.drop_index(op.f('ix_item_description'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # Drop enum type manually for postgres if needed, but Enum handles it usually
    sa.Enum(name='userrole').drop(op.get_bind())

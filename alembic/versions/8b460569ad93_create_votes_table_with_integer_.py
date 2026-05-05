"""create votes table with integer encrypted_vote

Revision ID: 8b460569ad93
Revises: 4cb39971ba5f
Create Date: 2026-04-25 11:10:45.303944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8b460569ad93'
down_revision: Union[str, Sequence[str], None] = '4cb39971ba5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Safely create the enum type - will not fail if it already exists
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE votestatus AS ENUM ('VALID', 'REJECTED');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    # Create the table
    op.create_table('votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('encrypted_vote', sa.Integer(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('status', postgresql.ENUM('VALID', 'REJECTED', name='votestatus', create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_votes_id'), 'votes', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_votes_id'), table_name='votes')
    op.drop_table('votes')
    # Safely drop the enum type
    op.execute("DROP TYPE IF EXISTS votestatus CASCADE")
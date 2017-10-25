"""create Package table.

Revision ID: 6daaf1d5cfee
Revises:
Create Date: 2017-10-17 15:48:05.193085

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6daaf1d5cfee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create table packages."""
    op.create_table(
        'packages',
        sa.Column(
            'id',
            sa.Integer,
            sa.Sequence('packages_id_seq', optional=True),
            primary_key=True
        ),
        sa.Column('name', sa.Unicode(255), nullable=False)
    )


def downgrade():
    """Drop table packages."""
    op.drop_table('packages')

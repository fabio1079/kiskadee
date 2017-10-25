"""add relation between fetchers and packages tables.

Revision ID: d2989db85795
Revises: 50988af48b09
Create Date: 2017-10-17 16:59:09.495015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2989db85795'
down_revision = '50988af48b09'
branch_labels = None
depends_on = None


def upgrade():
    """Add fetch_id to packages and set a unique constraint for it."""
    with op.batch_alter_table("packages") as batch_op:
        batch_op.add_column(
            sa.Column(
                'fetcher_id',
                sa.Integer,
                sa.ForeignKey('fetchers.id'),
                nullable=False
            )
        )
        batch_op.create_unique_constraint(
            'name_and_fetcher_id_unique',
            ['name', 'fetcher_id']
        )


def downgrade():
    """Undo add fetcher_id to packages."""
    with op.batch_alter_table("packages") as batch_op:
        op.drop_constraint('name_and_fetcher_id_unique', 'packages')
        batch_op.drop_column('fetcher_id')

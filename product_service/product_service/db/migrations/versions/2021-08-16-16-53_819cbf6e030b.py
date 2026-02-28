"""Initial migration.

Revision ID: 819cbf6e030b
Revises:
Create Date: 2021-08-16 16:53:05.484024

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "819cbf6e030b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Run the upgrade migrations."""
    op.create_table(
        "products",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("stock >= 0", name="ck_products_stock_non_negative"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reservations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("order_id", sa.UUID(), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("qty > 0", name="ck_reservations_qty_positive"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
    )
    op.create_index(
        op.f("ix_reservations_order_id"),
        "reservations",
        ["order_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_reservations_product_id"),
        "reservations",
        ["product_id"],
        unique=False,
    )


def downgrade() -> None:
    """Run the downgrade migrations."""
    op.drop_index(op.f("ix_reservations_product_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_order_id"), table_name="reservations")
    op.drop_table("reservations")
    op.drop_table("products")

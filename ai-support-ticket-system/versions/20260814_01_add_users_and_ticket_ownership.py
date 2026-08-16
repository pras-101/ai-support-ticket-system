"""Add users, authentication roles, and ticket ownership.

Revision ID: 20260814_01
Revises:
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa


revision = "20260814_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    table_names = inspector.get_table_names()

    if "users" not in table_names:
        user_role = sa.Enum("customer", "agent", "admin", name="user_role")
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("username", sa.String(length=50), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("role", user_role, nullable=False, server_default="customer"),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
            sa.UniqueConstraint("username", name="uq_users_username"),
        )
        op.create_index("ix_users_username", "users", ["username"])

    if "tickets" not in table_names:
        op.create_table(
            "tickets",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("customer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False, server_default="open"),
            sa.Column("priority", sa.String(length=32), nullable=True),
            sa.Column("category", sa.String(length=100), nullable=True),
            sa.Column("sentiment", sa.String(length=32), nullable=True),
            sa.Column("summary", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        )
        op.create_index("ix_tickets_customer_id", "tickets", ["customer_id"])
        return

    ticket_columns = {column["name"] for column in sa.inspect(bind).get_columns("tickets")}
    if "customer_id" not in ticket_columns:
        op.add_column("tickets", sa.Column("customer_id", sa.Integer(), nullable=True))
        op.create_foreign_key("fk_tickets_customer_id", "tickets", "users", ["customer_id"], ["id"])
        op.create_index("ix_tickets_customer_id", "tickets", ["customer_id"])


def downgrade() -> None:
    bind = op.get_bind()
    table_names = sa.inspect(bind).get_table_names()

    if "tickets" in table_names:
        ticket_columns = {column["name"] for column in sa.inspect(bind).get_columns("tickets")}
        if "customer_id" in ticket_columns:
            op.drop_index("ix_tickets_customer_id", table_name="tickets")
            op.drop_constraint("fk_tickets_customer_id", "tickets", type_="foreignkey")
            op.drop_column("tickets", "customer_id")

    if "users" in table_names:
        op.drop_index("ix_users_username", table_name="users")
        op.drop_table("users")
        sa.Enum(name="user_role").drop(bind, checkfirst=True)

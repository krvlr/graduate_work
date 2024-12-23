"""Added partitions for user_actions_history

Revision ID: c3641f5cd551
Revises: 7c21289c77c4
Create Date: 2023-06-18 11:33:02.468742

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c3641f5cd551"
down_revision = "7c21289c77c4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_roles_id"), ["id"])

    with op.batch_alter_table("user_actions_history", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f("uq_user_actions_history_id"), ["id", "created"]
        )

    with op.batch_alter_table("user_role", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_user_role_id"), ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user_role", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_user_role_id"), type_="unique")

    with op.batch_alter_table("user_actions_history", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_user_actions_history_id"), type_="unique")

    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_roles_id"), type_="unique")

    # ### end Alembic commands ###

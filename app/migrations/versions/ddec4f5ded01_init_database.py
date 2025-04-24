"""Init database

Revision ID: ddec4f5ded01
Revises:
Create Date: 2022-07-21 15:03:33.307447

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ddec4f5ded01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "rooms",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=600), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"))

    op.create_table(
        "entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=600), nullable=False),
        sa.Column("type", sa.Unicode(length=50), nullable=False),
        sa.Column("status", sa.Unicode(length=50), nullable=False),
        sa.Column("value", sa.String(length=600), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("room_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ),
        sa.PrimaryKeyConstraint("id"))

    op.create_index("entities_room_id_idx", "entities", ["room_id"], unique=False)

    # Set extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    # Populate database
    op.execute("insert into rooms values ('7609a74c-644e-480c-b32d-7eea7f27c773', 'Kitchen', '2020-01-01T00:00:00.000Z')")
    op.execute("insert into rooms values ('d9ec9a2f-6fd7-4e3c-ad29-7e293dcaa18d', 'Living Room', '2020-01-01T00:00:00.000Z')")
    op.execute("insert into rooms values ('51b7475f-d2d1-45b6-9303-33d7f3915f78', 'Bedroom', '2020-01-01T00:00:00.000Z')")
    op.execute("insert into rooms values ('a5a89aac-53f9-4b47-b14b-02e43c8ba6ad', 'Bathroom', '2020-01-01T00:00:00.000Z')")

    op.execute("insert into entities values (uuid_generate_v4(), 'Thermometer', 'sensor', 'on', '34.2', '2020-01-01 00:00:00', null)")
    op.execute("insert into entities values (uuid_generate_v4(), 'Kitchen light 1', 'light', 'off', null, '2020-01-01 00:00:00', '7609a74c-644e-480c-b32d-7eea7f27c773')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Living room light 1', 'light', 'on', '255', '2020-01-01 00:00:00', 'd9ec9a2f-6fd7-4e3c-ad29-7e293dcaa18d')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Living room light 2', 'light', 'off', null, '2020-01-01 00:00:00', 'd9ec9a2f-6fd7-4e3c-ad29-7e293dcaa18d')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Television', 'multimedia', 'on', 'TF1', '2020-01-01 00:00:00', 'd9ec9a2f-6fd7-4e3c-ad29-7e293dcaa18d')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Bedroom switch 1', 'switch', 'on', '1', '2020-01-01 00:00:00', '51b7475f-d2d1-45b6-9303-33d7f3915f78')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Bedroom light 1', 'light', 'unavailable', null, '2020-01-01 00:00:00', '51b7475f-d2d1-45b6-9303-33d7f3915f78')")
    op.execute("insert into entities values (uuid_generate_v4(), 'Air conditioner', 'air_conditioner', 'on', '24', '2020-01-01 00:00:00', '51b7475f-d2d1-45b6-9303-33d7f3915f78')")


def downgrade():
    op.drop_index("entities_room_id_idx", table_name="entities")
    op.drop_table("entities")
    op.drop_table("rooms")

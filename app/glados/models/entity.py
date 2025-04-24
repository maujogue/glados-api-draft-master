import uuid
from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID

from glados import db
from glados.models.abc import BaseModel


class Entity(db.Model, BaseModel):
    __tablename__ = "entities"
    __table_args__ = (
        Index("entities_room_id_idx", "room_id"),)

    to_json_filter = ["room"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(600), nullable=False)
    type = db.Column(db.Unicode(50), nullable=False)
    status = db.Column(db.Unicode(50), nullable=False)
    value = db.Column(db.String(600), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    room_id = db.Column(UUID(as_uuid=True), db.ForeignKey("rooms.id"), nullable=True)

    # Relationships
    room = db.relationship("Room", foreign_keys=[room_id], back_populates="entities")

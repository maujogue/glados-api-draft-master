import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from glados import db
from glados.models.abc import BaseModel


class Room(db.Model, BaseModel):
    __tablename__ = "rooms"

    to_json_filter = ["entities"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationships
    entities = db.relationship("Entity", back_populates="room", uselist=True)

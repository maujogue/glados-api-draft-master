from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType] + ["all"]))
    room = fields.String(required=False)
    status = fields.String(required=False, validate=validate.OneOf(["on", "off", "unavailable", "all"]))

class EntitiesTTSRequestSerializer(EntitiesRequestSerializer):
    language = fields.String(required=False, validate=validate.OneOf(["en-US", "fr-FR", "es-ES"]))
    voice = fields.String(required=False)
	
class EntityUpdateSerializer(ma.Schema):
    name = fields.String(required=False)
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room_id = fields.UUID(required=False, allow_none=True)
    
class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    """
    Serializer used for returning Entity objects in API responses.
    Inherits from EntitySerializer to include all the base Entity fields
    like id, name, type, status, value and created_at.
    """
    pass

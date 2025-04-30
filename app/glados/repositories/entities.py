from glados.models import Entity
from glados.models import Room

def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type and type != "all":
        query = query.filter(Entity.type == type)

    room = filters.get("room")
    if room and room != "all":
        room_obj = Room.query.get(room)
        if room_obj:
            query = query.filter(Entity.room_id == room_obj.id)

    status = filters.get("status")
    if status and status != "all":
        query = query.filter(Entity.status == status)

    return query

def update_entity_status(entity_id, new_status):
    entity = Entity.query.get(entity_id)
    if not entity:
        return None
    entity.status = new_status
    entity.save(commit=True)
    return entity

def update_entity_value(entity_id, new_value):
    entity = Entity.query.get(entity_id)
    if not entity:
        return None
    entity.value = new_value
    entity.save(commit=True)
    return entity

def get_all_rooms():
    rooms = Room.query.all()
    return [{"id": str(room.id), "name": room.name} for room in rooms]

def get_entity_by_id(entity_id):
    return Entity.query.get(entity_id)

def update_entity_general(entity_id, name=None, type=None, room_id=None):
    """
    Updates general attributes of an entity.

    Args:
        entity_id: UUID of the entity to update
        name: Optional new name for the entity
        type: Optional new type for the entity
        room_id: Optional UUID of room to assign entity to

    Returns:
        Updated Entity object if successful, None if entity not found

    Raises:
        Exception: If specified room_id does not exist
    """
    entity = Entity.query.get(entity_id)
    if not entity:
        return None
    if name is not None:
        entity.name = name
    if type is not None:
        entity.type = type
    if room_id is not None :
        if Room.query.get(room_id):
            entity.room_id = room_id
        else:
            raise Exception

    entity.save(commit=True)
    return entity

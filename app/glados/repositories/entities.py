from glados.models import Entity
from glados.models import Room

def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type and type != "all":
        query = query.filter(Entity.type == type)

    room = filters.get("room")
    if room and room != "all":
        room_obj = Room.query.filter(Room.name == room).first()
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
    return [r.name for r in Room.query.distinct(Room.name).all()]

import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=1),
        name="Ceiling Light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.off.name,
        value=None,
        room_id=kitchen.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id)
    entity.save(commit=False)


def test_get_entities_with_invalid_data(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_get_entities(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_type_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]

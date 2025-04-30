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


def test_get_entities_with_invalid_type(client):
    response = client.get("/entities?type=invalid")
    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner, all."]
    }}

def test_get_entities_with_invalid_status(client):
    response = client.get("/entities?status=invalid") 
    assert response.status_code == 422
    assert response.json == {"errors": {
        "status": ["Must be one of: on, off, unavailable, all."]
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


def test_get_entities_with_room_filter(client, entities, mocker):
    response = client.get("/entities?room=Kitchen")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_status_filter(client, entities, mocker):
    response = client.get("/entities?status=on")

    assert response.status_code == 200
    assert response.json == [
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


def test_get_entities_with_multiple_filters(client, entities, mocker):
    response = client.get("/entities?status=on&type=light&room=all")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp", 
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        }
    ]


def test_update_entity_name(client, entities, mocker):
    entity_id = "00000000-0000-0000-0000-000000000001"
    response = client.patch(f"/entities/{entity_id}", json={
        "name": "Updated Light"
    })

    assert response.status_code == 200
    assert response.json == {
        "id": entity_id,
        "name": "Updated Light",
        "type": "light",
        "status": "off",
        "value": None,
        "created_at": mocker.ANY
    }

def test_update_entity_type(client, entities, mocker):
    entity_id = "00000000-0000-0000-0000-000000000001"
    response = client.patch(f"/entities/{entity_id}", json={
        "type": "switch"
    })

    assert response.status_code == 200
    assert response.json == {
        "id": entity_id,
        "name": "Ceiling Light",
        "type": "switch",
        "status": "off",
        "value": None,
        "created_at": mocker.ANY
    }

def test_update_entity_room(client, entities, mocker):
    entity_id = "00000000-0000-0000-0000-000000000001"
    new_room_id = "00000000-0000-0000-0000-000000000002"  # Living Room
    response = client.patch(f"/entities/{entity_id}", json={
        "room_id": new_room_id
    })

    assert response.status_code == 200
    assert response.json == {
        "id": entity_id,
        "name": "Ceiling Light",
        "type": "light",
        "status": "off",
        "value": None,
        "created_at": mocker.ANY
    }

def test_update_entity_multiple_fields(client, entities, mocker):
    entity_id = "00000000-0000-0000-0000-000000000001"
    new_room_id = "00000000-0000-0000-0000-000000000002"  # Living Room
    response = client.patch(f"/entities/{entity_id}", json={
        "name": "New Light",
        "type": "switch",
        "room_id": new_room_id
    })

    assert response.status_code == 200
    assert response.json == {
        "id": entity_id,
        "name": "New Light",
        "type": "switch",
        "status": "off",
        "value": None,
        "created_at": mocker.ANY
    }

def test_update_entity_not_found(client):
    entity_id = "00000000-0000-0000-0000-000000000999"  # Non-existent ID
    response = client.patch(f"/entities/{entity_id}", json={
        "name": "New Name"
    })

    assert response.status_code == 404
    assert response.json == {"message": "Entity not found or update failed"}

def test_update_entity_invalid_type(client, entities):
    entity_id = "00000000-0000-0000-0000-000000000001"
    response = client.patch(f"/entities/{entity_id}", json={
        "type": "invalid_type"
    })

    assert response.status_code == 422
    assert "type" in response.json["errors"]

def test_update_entity_invalid_room(client, entities):
    entity_id = "00000000-0000-0000-0000-000000000001"
    response = client.patch(f"/entities/{entity_id}", json={
        "room_id": "00000000-0000-0000-0000-000000000999"  # Non-existent room
    })

    assert response.status_code == 404
    assert response.json == {"message": "Entity not found or update failed"}




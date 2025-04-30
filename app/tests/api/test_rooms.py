import uuid
import pytest

from glados.models import Room


@pytest.fixture
def rooms():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)


def test_get_rooms(client, rooms):
    response = client.get("/rooms")

    assert response.status_code == 200
    assert response.json == {
        "rooms": [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Kitchen"
            },
            {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room"
            }
        ]
    }

def test_add_room(client):
    response = client.post("/rooms", json={"name": "Bedroom"})

    assert response.status_code == 201
    assert response.json["name"] == "Bedroom"

def test_delete_room(client, rooms):
    room_id = "00000000-0000-0000-0000-000000000001"  # Kitchen
    response = client.delete(f"/rooms/{room_id}")

    assert response.status_code == 200
    assert response.json == {"message": "Room deleted"}

def test_edit_room(client, rooms):
    room_id = "00000000-0000-0000-0000-000000000001"  # Kitchen
    response = client.patch(f"/rooms/{room_id}", json={"name": "Updated Kitchen"})

    assert response.status_code == 200
    assert response.json["name"] == "Updated Kitchen"

def test_edit_room_name_conflict(client, rooms):
    room_id = "00000000-0000-0000-0000-000000000001"  # Kitchen
    response = client.patch(f"/rooms/{room_id}", json={"name": "Living Room"})

    assert response.status_code == 409
    assert response.json == {"message": "Room name already taken"}
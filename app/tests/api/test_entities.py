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
    response = client.get(f"/entities?room={uuid.UUID(int=1)}")

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

def test_entities_tts_success(client, entities, mocker):
    # Mock Gemini API response
    mocker.patch("requests.post", return_value=mocker.Mock(json=lambda: {
        "candidates": [{"content": {"parts": [{"text": "Summary from Gemini."}]}}]
    }))
    # Mock Google TTS response
    class FakeTTSResponse:
        audio_content = b"fake-audio"
    mock_tts_client = mocker.Mock()
    mock_tts_client.synthesize_speech.return_value = FakeTTSResponse()
    mocker.patch("google.cloud.texttospeech.TextToSpeechClient", return_value=mock_tts_client)

    response = client.get("/entities/tts?language=en-US")
    assert response.status_code == 200
    data = response.json
    assert "summary" in data and data["summary"] == "Summary from Gemini."
    assert "audio_base64" in data and data["audio_base64"]
    assert data["language"] == "en-US"
    assert data["voice"] == "default"

def test_entities_tts_gemini_error(client, entities, mocker):
    # Patch Gemini API to raise error
    mocker.patch("requests.post", side_effect=Exception("Gemini down"))
    response = client.get("/entities/tts?language=en-US")
    assert response.status_code == 503
    assert "Gemini API error" in response.json["error"]

def test_entities_tts_tts_error(client, entities, mocker):
    # Mock Gemini API response
    mocker.patch("requests.post", return_value=mocker.Mock(json=lambda: {
        "candidates": [{"content": {"parts": [{"text": "Summary from Gemini."}]}}]
    }))
    # Patch TTS to raise error
    mocker.patch("google.cloud.texttospeech.TextToSpeechClient", side_effect=Exception("TTS down"))
    response = client.get("/entities/tts?language=en-US")
    assert response.status_code == 500
    assert "TTS API error" in response.json["error"]




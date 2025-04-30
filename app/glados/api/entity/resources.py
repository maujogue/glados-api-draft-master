from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntityUpdateSerializer
from glados.repositories.entities import get_entities, update_entity_status, update_entity_value, get_all_rooms, get_entity_by_id, update_entity_general
from glados import constants
from glados.models.room import Room
from marshmallow import ValidationError


class EntitiesAPI(Resource):
	def get(self):
		request_serializer = EntitiesRequestSerializer()
		data = request_serializer.load(request.args)

		entities = get_entities(data)

		if not entities:
			return {"message": "No entities found", "data": []}, 200
		serializer = EntityResponseSerializer(many=True)
		return serializer.dump(entities), 200

	def patch(self):
		data = request.get_json()
		entity_id = data.get("id")
		new_status = data.get("status")
		new_value = data.get("value")
		if not entity_id or (new_status is None and new_value is None):
			return {"message": "Missing id or update fields"}, 400
		entity = None
		if new_status is not None:
			entity = update_entity_status(entity_id, new_status)
		if new_value is not None:
			entity = update_entity_value(entity_id, new_value)
		if not entity:
			return {"message": "Entity not found"}, 404
		serializer = EntityResponseSerializer()
		return serializer.dump(entity), 200

class RoomsAPI(Resource):
	def get(self):
		rooms = Room.query.all()
		return {"rooms": [{"id": str(room.id), "name": room.name} for room in rooms]}

class TypesAPI(Resource):
	def get(self):
		types = [t.name for t in constants.EntityType]
		return {"types": types}, 200

class EntityAPI(Resource):
	def patch(self, entity_id):
		data = request.get_json()
		serializer = EntityUpdateSerializer()
		try:
			validated_data = serializer.load(data)
		except ValidationError as err:
			return {"errors": err.messages}, 422

		try:
			entity = update_entity_general(
				entity_id,
				name=validated_data.get("name"),
				type=validated_data.get("type"),
				room_id=validated_data.get("room_id"),
			)
			if not entity:
				raise Exception
		except Exception as e:
			return {"message": "Entity not found or update failed"}, 404

		response_serializer = EntityResponseSerializer()
		return response_serializer.dump(entity), 200

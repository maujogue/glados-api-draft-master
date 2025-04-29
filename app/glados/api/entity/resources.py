from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer
from glados.repositories.entities import get_entities, update_entity_status, update_entity_value, get_all_rooms
from glados import constants


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
		rooms = get_all_rooms()
		return {"rooms": rooms}, 200

class TypesAPI(Resource):
	def get(self):
		types = [t.name for t in constants.EntityType]
		return {"types": types}, 200

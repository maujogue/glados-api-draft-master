from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer
from glados.repositories.entities import get_entities


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

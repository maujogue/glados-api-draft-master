from flask import Blueprint
from flask_restful import Api

from glados.api.misc import resources as misc_resources
from glados.api.entity import resources as entity_resources
from glados.api.room import resources as room_resources

blueprint = Blueprint("api", __name__)
api = Api(blueprint)

# Misc endpoints
api.add_resource(misc_resources.VersionAPI, "/")

# Entities endpoints
api.add_resource(entity_resources.EntitiesAPI, "/entities")
api.add_resource(entity_resources.EntitiesTTSAPI, "/entities/tts")
api.add_resource(entity_resources.EntityAPI, "/entities/<string:entity_id>")
api.add_resource(entity_resources.TypesAPI, "/entities/types")

# Room endpoints
api.add_resource(room_resources.RoomAPI, "/room", "/room/<string:room_id>")
api.add_resource(room_resources.RoomsAPI, "/rooms")


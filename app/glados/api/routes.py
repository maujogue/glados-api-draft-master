from flask import Blueprint
from flask_restful import Api

from glados.api.misc import resources as misc_resources
from glados.api.entity import resources as entity_resources

blueprint = Blueprint("api", __name__)
api = Api(blueprint)

# Misc endpoints
api.add_resource(misc_resources.VersionAPI, "/")

# Entities endpoints
api.add_resource(entity_resources.EntitiesAPI, "/entities")

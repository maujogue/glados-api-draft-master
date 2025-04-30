from flask import request
from flask_restful import Resource
from glados.models.room import Room
from glados import db

class RoomAPI(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        if not name:
            return {"message": "Room name is required"}, 400
        room = Room(name=name)
        db.session.add(room)
        db.session.commit()
        return {"id": str(room.id), "name": room.name}, 201

    def delete(self, room_id):
        room = Room.query.get(room_id)
        if not room:
            return {"message": "Room not found"}, 404
        db.session.delete(room)
        db.session.commit()
        return {"message": "Room deleted"}, 200

    def patch(self, room_id):
        data = request.get_json()
        name = data.get("name")
        if not name:
            return {"message": "Room name is required"}, 400

        existing_room = Room.query.filter_by(name=name).first()
        if existing_room:
            return {"message": "Room name already taken"}, 409

        room = Room.query.get(room_id)
        if not room:
            return {"message": "Room not found"}, 404

        room.name = name
        db.session.commit()
        return {"id": str(room.id), "name": room.name}, 200

class RoomsAPI(Resource):
	def get(self):
		rooms = Room.query.all()
		return {"rooms": [{"id": str(room.id), "name": room.name} for room in rooms]}
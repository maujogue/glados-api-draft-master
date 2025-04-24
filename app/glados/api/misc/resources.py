from flask_restful import Resource


class VersionAPI(Resource):
    def get(self):
        return {"version": "1.0"}

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs.serving import response_quote
from src.models.user import UserModel
from src.models.ads import AdsModel

class AdsList(Resource):

    @classmethod
    def get(cls):
        return {"users_requests": [user_request.turn_to_json() for user_request in AdsModel.query.all()]}, 200


class AdsCreation(Resource):

    @classmethod
    #@jwt_required
    def post(cls):
        #user = get_jwt_identity()
        data = request.get_json()

        #if not UserModel.find_by_session_key(user):
            #return {"message": response_quote("code_401")}, 401

        user_request = AdsModel(
            theme=data["theme"],
            body=data["body"],
            status=data["status"]
        )
        user_request.save_to_db()

        return {"msg": "ad created"}, 1



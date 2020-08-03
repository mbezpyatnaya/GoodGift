from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs.serving import response_quote
from src.user.models import UserModel
from src.requests.models import RequestModel


class RequestsList(Resource):

    @classmethod
    def get(cls):
        return {"users_requests": [user_request.turn_to_json() for user_request in RequestModel.query.all()]}, 200


class RequestCreation(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        session_key = get_jwt_identity()
        data = request.get_json()
        user = UserModel.find_by_session_key(session_key)
        if not user:
            return {"message": response_quote("code_401")}, 401

        user_request = RequestModel(
            theme=data["theme"],
            body=data["body"],
            status=data["status"],
            creator=user.id
        )
        user_request.save_to_db()

        return {"msg": "request created"}, 201



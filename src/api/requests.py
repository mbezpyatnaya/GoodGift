from flask import request, render_template
from flask_restful import Resource
from src.models.user import UserModel
from src.models.requests import RequestModel


class RequestsList(Resource):

    @classmethod
    def get(cls):
        return {"users_requests": [user_request.turn_to_json() for user_request in RequestModel.query.all()]}, 200


class RequestCreation(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()
        print(data)

        user_request = RequestModel(
            theme=data["theme"],
            body=data["body"],
            status=data["status"]
        )

        user_request.save_to_db()

        return {"msg": "request created"}, 201



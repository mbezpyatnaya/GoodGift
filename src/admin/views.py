from flask import request
from flask_restful import Resource

from libs.passhash import PassCrypt
from libs.serving import response_quote
from src.user.models import UserModel
from src.email.confirmations.models import ConfirmationModel


class SuperUser(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()

        if UserModel.find_by_email(data['email']):
            return {"message": response_quote("user_email_taken")}, 400

        password_salt, password_hash = PassCrypt.generate_password_hash(data["password"])
        superuser = UserModel(
            username=data["username"],
            email=data["email"],
            password_hash=password_hash,
            password_salt=password_salt
        )

        superuser.save_to_db()
        confirmation = ConfirmationModel(superuser.id)
        confirmation.confirmed = True
        confirmation.save_to_db()

        return {"message": response_quote("user_been_created")}, 201

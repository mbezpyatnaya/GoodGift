from flask import request, render_template
from flask_restful import Resource
from src.models.user import UserModel, RequestModel

class Request(Resource):
    def post(self):
        data = self.parser.parse_args()
        title = data['title']
        content = data['content']
        price = data['price']
        username = data['username']
        post_type = data['post_type']
        # Missing Parameters
        if title is None or content is None or username is None:
            return {'message': 'No title or content or creator passed for create record.'}, 400

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {'message': f'User {username} not found.'}, 401

            request = RequestModel()
            request.title = title
            request.posted_by_id = user.id
            request.content = content
            request.status = 1
        
            db.session.add(request)
            db.session.commit()

        return {'message': 'Post created.'}, 200
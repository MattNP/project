# -*- coding: utf-8 -*
from flask import jsonify, request
from flask_restful import Resource
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user_data = User.query.get([user_id])
            user_data = user_schema.dump(user_data).data
        else:
            user_data = User.query.all()
            user_data = users_schema.dump(user_data).data
        return {"status":"success", "data":user_data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        user = User.query.filter_by(id=data['user_id']).first()
        if user:
            return {'message': 'Category already exists'}, 400
        user = User(
            name=json_data['name']
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return { "status": 'success', 'data': result }, 201


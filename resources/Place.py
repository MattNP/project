# -*- coding: utf-8 -*
from flask import request
from flask_restful import Resource
from Model import db, Place, PlaceSchema

places_schema = PlaceSchema(many=True)
place_schema = PlaceSchema()

class PlaceResource(Resource):
    def get(self, place_id=None):
        if place_id:
            place_data = Place.query.get([place_id])
            place_data = place_schema.dump(place_data).data
        else:
            place_data = Place.query.all()
            place_data = places_schema.dump(place_data).data
        return {"status":"success", "data":place_data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = place_schema.load(json_data)
        if errors:
            return errors, 422
        place = Place.query.filter_by(name=data['name']).first()
        if place:
            return {'message': 'Place already exists'}, 400
        place = Place(
            name=json_data['name']
            )

        db.session.add(place)
        db.session.commit()

        result = place_schema.dump(place).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = place_schema.load(json_data)
        if errors:
            return errors, 422
        place = Place.query.filter_by(id=data['id']).first()
        if not place:
            return {'message': 'Place does not exist'}, 400
        place.name = data['name']
        db.session.commit()

        result = place_schema.dump(place).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = place_schema.load(json_data)
        if errors:
            return errors, 422
        place = Place.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = place_schema.dump(place).data

        return { "status": 'success', 'data': result}, 204

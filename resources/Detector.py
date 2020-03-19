# -*- coding: utf-8 -*
from flask import jsonify, request
from flask_restful import Resource
from Model import db, Detector, Place, DetectorSchema

detectors_schema = DetectorSchema(many=True)
detector_schema = DetectorSchema()

class DetectorResource(Resource):
    def get(self, detector_id=None):
        if detector_id:
            detector_data = Detector.query.get([detector_id])
            detector_data = detector_schema.dump(detector_data).data
        else:
            detector_data = Detector.query.all()
            detector_data = detectors_schema.dump(detector_data).data
        return {"status":"success", "data":detector_data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = detector_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        place_id = Place.query.filter_by(id=data['place_id']).first()
        if not place_id:
            return {'status': 'error', 'message': 'detector place not found'}, 4

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = detector_schema.load(json_data)
        if errors:
            return errors, 422
        detector = Detector.query.filter_by(id=data['id']).first()
        if not detector:
            return {'message': 'Detector does not exist'}, 400
        detector.status = data['status']
        db.session.commit()

        result = detector_schema.dump(detector).data

        return { "status": 'success', 'data': result }, 204
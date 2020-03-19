# -*- coding: utf-8 -*
from flask import request
from flask_restful import Resource
from Model import db, Alert, AlertSchema
from random import randint

alerts_schema = AlertSchema(many=True)
alert_schema = AlertSchema()

class AlertResource(Resource):
    def get(self, alert_id=None):
        if alert_id:
            alert_data = Alert.query.get([alert_id])
            alert_data = alert_schema.dump(alert_data).data
        else:
            alert_data = Alert.query.all()
            alert_data = alerts_schema.dump(alert_data).data
        return {"status":"success", "data":alert_data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = alert_schema.load(json_data)
        if errors:
            return errors, 422
        alert = Alert(
            id=str(randint(1, 10000)),
            message=json_data['message'],
            detector_id=json_data['detector_id']
        )

        db.session.add(alert)
        db.session.commit()

        result = alert_schema.dump(alert).data

        return { "status": 'success', 'data': result }, 201
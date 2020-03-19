# -*- coding: utf-8 -*
from simplexml import dumps
from flask import Blueprint, make_response
from flask_restful import Api
from resources.Hello import Hello
from resources.Place import PlaceResource
from resources.Detector import DetectorResource
from resources.User import UserResource
from resources.Alert import AlertResource

def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response':data}), code)
    resp.headers.extend(headers or {})
    return resp

#api_bp = Blueprint('api', __name__)
#api = Api(api_bp, default_mediatype='application/xml')
#api.representations['application/xml'] = output_xml

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(PlaceResource, '/Place', '/Place/', '/Place/<place_id>')
api.add_resource(DetectorResource, '/Detector', '/Detector/', '/Detector/<detector_id>')
api.add_resource(UserResource, '/User', '/User/', '/User/<user_id>')
api.add_resource(AlertResource, '/Alert')

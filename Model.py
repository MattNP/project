# -*- coding: utf-8 -*
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Detector(db.Model):
    __tablename__ = 'detectors'
    id = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    place_id = db.Column(db.String(), db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    place = db.relationship('Place', backref=db.backref('detectors', lazy='dynamic' ))

    def __init__(self, description, brand, status, place_id):
        self.description = description
        self.brand = brand
        self.status = status
        self.place_id = place_id


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Numeric(), nullable=False)
    latitude = db.Column(db.Numeric(), nullable=False)
    def __init__(self, name, location, status, longitude, latitude):
        self.name = name
        self.location = location
        self.status = status
        self.longitude = longitude
        self.latitude = latitude

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.String(), primary_key=True)
    message = db.Column(db.String(240), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    detector_id = db.Column(db.String(), db.ForeignKey('detectors.id', ondelete='CASCADE'), nullable=False)
    detector = db.relationship('Detector', backref=db.backref('alerts', lazy='dynamic' ))
    def __init__(self, id, message, detector_id):
        self.id = id
        self.message = message
        self.detector_id = detector_id

detector_user = db.Table('detector_user',
    db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('detector_id', db.String, db.ForeignKey('detectors.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(), primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    detectors = db.relationship('Detector', secondary=detector_user)
    def __init__(self, login, password, name, role):
        self.login = login
        self.password = password
        self.name = name
        self.role = role

class PlaceSchema(ma.Schema):
    id = fields.String()
    name = fields.String(required=True)
    location = fields.String(required=True)
    status = fields.String(required=True)
    longitude = fields.Number(required=True)
    latitude = fields.Number(required=True)

class DetectorSchema(ma.Schema):
    id = fields.String()
    brand = fields.String(required=True)
    status = fields.String(required=True)
    place_id = fields.String(required=True)

class AlertSchema(ma.Schema):
    id = fields.String()
    message = fields.String(required=True)
    detector_id = fields.String(required=True)
    timestamp = fields.DateTime()

class UserSchema(ma.Schema):
    id = fields.String()
    login = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)
    role = fields.String(required=True)
    detectors = fields.List(fields.Nested(DetectorSchema), required=True)

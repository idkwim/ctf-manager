#!/usr/bin/env python
from app import db

class CtfAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(60))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<CtfAdmin: %s>' % self.username

class CtfEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    type = db.Column(db.String(30))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    details = db.Column(db.String())
    url = db.Column(db.String())
    login = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, type, start_date, end_date, url, login, password):
        self.name = name
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.login = login
        self.password = password

    def __repr__(self):
        return '<CtfEvent: %s>' % self.name

class CtfEventChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_code = db.Column(db.String())
    category = db.Column(db.String())
    point_value = db.Column(db.Integer)
    assigned = db.Column(db.String())

    def __init__(self, event_code, category, point_value, assigned):
        self.event_code = event_code
        self.category = category
        self.point_value = point_value
        self.assigned = assigned

    def __repr__(self):
        return '<CtfEventChallenge: %s-%s-%s>' % (self.event_code, self.category, self.point_value)

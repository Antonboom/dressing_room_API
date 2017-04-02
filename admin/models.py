# -*- coding: utf-8 -*-

from application import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __unicode__(self):
        return self.login

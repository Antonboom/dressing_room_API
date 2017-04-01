# -*- coding: utf-8 -*-

from application import db


class Color(db.Model):

    __table_name__ = 'color'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hex = db.Column(db.String(64))
    rgb = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64))

    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id = parent_id

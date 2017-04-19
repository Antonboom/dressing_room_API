# -*- coding: utf-8 -*-

from application import db


class Color(db.Model):

    __tablename__ = 'color'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    hex = db.Column(db.String(32))
    rgb = db.Column(db.String(32))

    def __init__(self, name, hex=None, rgb=None):
        self.name = name
        self.hex = hex
        self.rgb = rgb

# -*- coding: utf-8 -*-

from application import db


class Color(db.Model):

    __tablename__ = 'color'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    hex = db.Column(db.String(32))
    rgb = db.Column(db.String(32))

    color_ratios = db.relationship('ClothingColorRatio', backref=db.backref('color'))

    def __init__(self, name, hex=None, rgb=None):
        self.name = name
        self.hex = hex
        self.rgb = rgb

    def __repr__(self):
        return '<Color "{}, #{}">'.format(self.name, self.hex)

    def serialize(self):
        return {
            'id': self.id,
            'hex': self.hex
        }

# -*- coding: utf-8 -*-

from application import db


class ClothingColorRatio(db.Model):

    __tablename__ = 'clothing_color_ratio'

    id = db.Column(db.Integer, primary_key=True)

    is_active = db.Column(db.Boolean, default=True)

    rule_id = db.Column(db.Integer, db.ForeignKey('fashion_rule.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

# -*- coding: utf-8 -*-

from application import db


class ClothingColorRatio(db.Model):

    __tablename__ = 'clothing_color_ratio'

    id = db.Column(db.Integer, primary_key=True)

    is_active = db.Column(db.Boolean, default=True)

    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return '<Цветовое соотношение {} "{} - {}">'.format(self.id, self.color, self.category)

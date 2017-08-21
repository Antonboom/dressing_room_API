# -*- coding: utf-8 -*-

from application import db


class FashionSeason(db.Model):

    __tablename__ = 'fashion_season'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), nullable=False)

    start = db.Column(db.Date, nullable=True)
    end = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    rules = db.relationship('FashionRule', backref='season', lazy='dynamic', cascade='delete')

    def __repr__(self):
        return '<Сезон {} "{}">'.format(self.id, self.name)

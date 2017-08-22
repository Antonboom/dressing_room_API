# -*- coding: utf-8 -*-

import time

import models as m
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

    @property
    def active_rules(self):
        return self.rules.filter(m.FashionRule.is_active.is_(True)).all()

    def get_compatibility_percentage(self, pids):
        rules_count = len(list(self.active_rules))
        rules_percentage = sum(rule.get_compatibility_percentage(pids) for rule in self.active_rules)

        return round(rules_percentage / rules_count, 4)

    def serialize(self, pids=None):
        return {
            'id': self.id,
            'name': self.name,
            'start': time.mktime(self.start.timetuple()),
            'end': time.mktime(self.end.timetuple()),
            'is_active': self.is_active,
            'fashion_rules': [rule.serialize(pids) for rule in self.active_rules]
        }

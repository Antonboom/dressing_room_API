# -*- coding: utf-8 -*-

import models as m
from application import db


rule_color_ratio = db.Table('rule_clothing_color_ratio',
    db.Column('rule_id', db.Integer, db.ForeignKey('fashion_rule.id')),
    db.Column('color_ratio_id', db.Integer, db.ForeignKey('clothing_color_ratio.id')),
    db.UniqueConstraint('rule_id', 'color_ratio_id', name='US_rule_id_color_ratio_id')
)


class FashionRule(db.Model):

    __tablename__ = 'fashion_rule'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    season_id = db.Column(db.Integer, db.ForeignKey('fashion_season.id'), nullable=False)
    color_ratios = db.relationship('ClothingColorRatio', secondary=rule_color_ratio, backref=db.backref('rules', lazy='dynamic'))

    def __repr__(self):
        return '<Правило моды {} "{}">'.format(self.id, self.name)

    def get_compatibility_percentage(self, pids):
        """
        :type pids: (list|tuple)
        """

        ratios_usage = dict.fromkeys([ratio.id for ratio in self.color_ratios], 0)
        products_usage = dict.fromkeys(pids, 0)

        for product_id in pids:
            product = m.Product.query.get(product_id)
            for color_ratio in self.color_ratios:
                if product.is_fits_color_ratio(color_ratio):
                    products_usage[product_id] += 1
                    ratios_usage[color_ratio.id] += 1

        ratios_count = len(self.color_ratios)
        ratios_usage_count = len(list(filter(lambda item: item[1] != 0, ratios_usage.items())))

        products_count = len(pids)
        products_usage_count = len(list(filter(lambda item: item[1] != 0, products_usage.items())))

        return (ratios_usage_count / ratios_count + products_usage_count / products_count) / 2.

    def serialize(self, pids=None):
        data = {
            'name': self.name,
            'is_active': self.is_active
        }

        if pids:
            data['compatibility'] = round(self.get_compatibility_percentage(pids), 4)

        return data

# -*- coding: utf-8 -*-

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

    season_id = db.Column(db.Integer, db.ForeignKey('fashion_season.id'))
    color_ratios = db.relationship('ClothingColorRatio', secondary=rule_color_ratio, backref=db.backref('rules', lazy='dynamic'))

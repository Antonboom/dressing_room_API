# -*- coding: utf-8 -*-

from application import db


class Category(db.Model):

    __table_name__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    childrens = db.relationship('Category', backref=db.backref('parent', remote_side=id), cascade="delete")

    gender = db.Column(db.String(64), nullable=False)
    is_childish = db.Column(db.Boolean, default=False)

    lamoda_url = db.Column(db.String(256), nullable=True, unique=True)

    goods = db.relationship('Good', backref=db.backref('category'))

    def __init__(self, name, parent_id, gender, id=None, lamoda_url=None, is_childish=False):
        if id:
            self.id = id

        self.name = name
        self.parent_id = parent_id
        self.gender = gender
        self.lamoda_url = lamoda_url
        self.is_childish = is_childish

    def __repr__(self):
        return '<Category "{}">'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'gender': self.gender,
            'is_childish': self.is_childish,
            'childrens': len(self.childrens),
            'goods': len(self.goods),
        }

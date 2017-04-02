# -*- coding: utf-8 -*-

from application import db


colors = db.Table('colors',
    db.Column('good_id', db.Integer, db.ForeignKey('good.id')),
    db.Column('color_id', db.Integer, db.ForeignKey('color.id'))
)


class Good(db.Model):

    __table_name__ = 'good'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(256), nullable=False)
    uv_card = db.Column(db.String(256))
    url = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(1024))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    colors = db.relationship('Color', secondary=colors, backref=db.backref('goods', lazy='dynamic'))

    def __init__(self, name, price, photo, url, category_id, description=None):
        self.name = name
        self.price = price
        self.photo = photo
        self.url = url
        self.category_id = category_id
        self.description = description

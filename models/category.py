# -*- coding: utf-8 -*-

from application import db


category_size = db.Table('category_size',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('size_id', db.Integer, db.ForeignKey('size.id')),
    db.UniqueConstraint('category_id', 'size_id', name='US_category_id_size_id')
)


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    childrens = db.relationship('Category', backref=db.backref('parent', remote_side=id), cascade='delete')

    gender = db.Column(db.String(64), nullable=False)
    is_childish = db.Column(db.Boolean, default=False)

    lamoda_url = db.Column(db.String(256), nullable=True, unique=True)

    products = db.relationship('Product', backref=db.backref('category'))
    sizes = db.relationship('Size', secondary=category_size, lazy='dynamic', backref=db.backref('categories'))

    def __init__(self, name, parent_id, gender, id=None, lamoda_url=None, is_childish=False):
        if id:
            self.id = id

        self.name = name
        self.parent_id = parent_id
        self.gender = gender
        self.lamoda_url = lamoda_url
        self.is_childish = is_childish

    def __repr__(self):
        return '<Category {} "{}">'.format(self.id, self.name)

    @classmethod
    def top_level(cls):
        return cls.query.filter(cls.parent_id.is_(None)).all()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'gender': self.gender,
            'is_childish': self.is_childish,
            'childrens': len(self.childrens),
            'products': len(self.products),
        }

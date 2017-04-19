# -*- coding: utf-8 -*-

import os
import hashlib

from urllib import request
from urllib.parse import urljoin

import settings

from application import db
from models.mixins import SetFieldsMixin


product_color = db.Table('product_color',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('color_id', db.Integer, db.ForeignKey('color.id'))
)


class Product(SetFieldsMixin, db.Model):

    __table_name__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(256))
    uv_card = db.Column(db.String(256))
    url = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text(1024))

    gender = db.Column(db.String(64), nullable=False)
    is_childish = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    colors = db.relationship('Color', secondary=product_color, backref=db.backref('goods', lazy='dynamic'))

    # Брюки
    height = db.Column(db.SmallInteger)                      # Высота
    inner_seam_length = db.Column(db.SmallInteger)           # Длина по внутреннему шву
    along_side_seam_length = db.Column(db.SmallInteger)      # Длина по боковому шву
    circumference_at_waist = db.Column(db.SmallInteger)      # Обхват по талии
    circumference_at_hips = db.Column(db.SmallInteger)       # Обхват по бедрам
    bottom_width = db.Column(db.SmallInteger)              # Обхват по низу

    # Верхняя одежда
    length = db.Column(db.SmallInteger)                      # Длина

    required_fields = (
        'name',
        'price',
        'gender',
        'is_childish',
        'category_id',
        'source_id'
    )

    not_required_fields = (
        'url',
        'description',

        'height',
        'inner_seam_length',
        'along_side_seam_length',
        'circumference_at_waist',
        'circumference_at_hips',
        'bottom_width'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product "{}:{}">'.format(self.name, self.url)

    def set_photo(self, photo_url):
        photo_file_name = hashlib.sha256(str(self.url).encode('utf-8')).hexdigest() + '.jpeg'
        photo_path = os.path.join(settings.STATIC_PATH, 'images', 'products', 'photo', photo_file_name)

        response = request.urlopen(photo_url)
        photo_data = response.read()

        with open(photo_path, 'wb') as photo:
            photo.write(photo_data)
        photo.close()

        photo_url = urljoin(settings.STATIC_URL, 'products') + '/' + photo_file_name

        self.photo = photo_url

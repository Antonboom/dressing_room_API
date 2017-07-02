# -*- coding: utf-8 -*-

import os
import hashlib
import logging

from urllib import request
from urllib.parse import urljoin

import settings

from application import db
from models.mixins import SetFieldsMixin


logger = logging.getLogger(__name__)


product_color = db.Table('product_color',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('color_id', db.Integer, db.ForeignKey('color.id')),
    db.UniqueConstraint('product_id', 'color_id', name='US_product_id_color_id')
)


product_size = db.Table('product_size',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('size_id', db.Integer, db.ForeignKey('size.id')),
    db.UniqueConstraint('product_id', 'size_id', name='US_product_id_size_id')
)


class Product(SetFieldsMixin, db.Model):

    __table_name__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(256))
    uv_card = db.Column(db.String(256))
    url = db.Column(db.String(256), unique=True)
    description = db.Column(db.Text(1024))

    gender = db.Column(db.String(64), nullable=False)
    is_childish = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    colors = db.relationship('Color', secondary=product_color, backref=db.backref('goods', lazy='dynamic'))

    sizes = db.relationship('Size', secondary=product_size, backref=db.backref('products', lazy='dynamic'))

    # Брюки
    height = db.Column(db.SmallInteger)                      # Высота
    inner_seam_length = db.Column(db.SmallInteger)           # Длина по внутреннему шву
    along_side_seam_length = db.Column(db.SmallInteger)      # Длина по боковому шву
    waist_girth = db.Column(db.SmallInteger)                 # Обхват по талии
    hip_girth = db.Column(db.SmallInteger)                   # Обхват по бедрам
    bottom_width = db.Column(db.SmallInteger)                # Ширина по низу

    # Верхняя одежда
    length = db.Column(db.SmallInteger)                      # Длина
    sleeve_length = db.Column(db.SmallInteger)               # Длина рукава

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
        'waist_girth',
        'hip_girth',
        'bottom_width',

        'length',
        'sleeve_length',
    )

    BASE_PHOTO_PATH = os.path.join(settings.STATIC_PATH, 'images', 'products', 'photo')
    BASE_UV_CARD_PATH = os.path.join(settings.STATIC_PATH, 'images', 'products', 'uv_card')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product "{}:{}">'.format(self.name, self.url)

    def set_photo(self, photo_url):
        photo_file_name = hashlib.sha256(photo_url.encode('utf-8')).hexdigest() + '.jpeg'
        photo_path = os.path.join(self.BASE_PHOTO_PATH, photo_file_name)

        logging.debug('Loading product photo from {}'.format(photo_url))

        response = request.urlopen(photo_url, timeout=10)
        photo_data = response.read()

        with open(photo_path, 'wb') as photo:
            photo.write(photo_data)
        photo.close()

        logging.debug('Save product photo to {}'.format(photo_path))

        self.photo = photo_file_name

    @property
    def photo_url(self):
        if self.photo.startswith('http'):
            return self.photo
        return urljoin(settings.STATIC_URL, 'products') + '/' + self.photo

    @property
    def uv_card_url(self):
        return urljoin(settings.STATIC_URL, 'uv_card') + '/' + self.uv_card if self.uv_card else ''

    @property
    def uv_card_path(self):
        return os.path.join(self.BASE_UV_CARD_PATH, self.uv_card) if self.uv_card else ''

    @property
    def top_level_category_id(self):
        category = self.category
        while category.parent:
            category = category.parent
        return category.id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'photo': self.photo_url,
            'uv_card': self.uv_card_url,
            'url': self.url,
            'description': self.description,
            'category': self.category_id
        }

    def full_serialize(self):
        data = self.serialize()

        data['colors'] = [color.serialize() for color in self.colors]
        data['sizes'] = [size.serialize() for size in self.sizes]
        data['top_level_category'] = self.top_level_category_id

        return data

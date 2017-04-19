# -*- coding: utf-8 -*-

from application import db
from models.mixins import SetFieldsMixin


class Size(SetFieldsMixin, db.Model):

    __tablename__ = 'size'

    id = db.Column(db.Integer, primary_key=True)

    chest_girth = db.Column(db.Float)                           # Обхват груди
    waist_girth = db.Column(db.Float, nullable=False)           # Обхват талии
    hip_girth = db.Column(db.Float, nullable=False)             # Обхват бедер
    sleeve_length = db.Column(db.String(32))                    # Длина рукава

    russia = db.Column(db.SmallInteger, nullable=False)         # Размер в России
    europe = db.Column(db.SmallInteger)                         # Размер в Европе
    uk = db.Column(db.SmallInteger)                             # Размер в Великобритании
    usa = db.Column(db.SmallInteger)                            # Размер в США
    international = db.Column(db.String(32), nullable=False)    # Международное обозначение

    required_fields = (
        'waist_girth',
        'hip_girth',
        'russia',
        'international'
    )

    not_required_fields = (
        'chest_girth',
        'sleeve_length',
        'europe',
        'uk',
        'usa'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Size "Russia: {}, {}">'.format(self.russia, self.international)

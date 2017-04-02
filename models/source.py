# -*- coding: utf-8 -*-

from application import db


class Source(db.Model):

    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    site_url = db.Column(db.String(128), unique=True, nullable=False)
    logo_url = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    goods = db.relationship('Good', backref=db.backref('source'))

    def __init__(self, name, site_url, logo_url, is_active=False):
        self.name = name
        self.site_url = site_url
        self.logo_url = logo_url
        self.is_active = is_active

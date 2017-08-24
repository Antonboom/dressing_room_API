# -*- coding: utf-8 -*-

import uuid

from datetime import datetime

from application import db


__all__ = [
    'UserSession'
]


def hex_uuid():
    return uuid.uuid4().hex


class UserSession(db.Model):

    __tablename__ = 'user_session'

    id = db.Column(db.Integer, primary_key=True)

    uid = db.Column(db.String(32), index=True, default=hex_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    actions = db.relationship('UserAction', backref=db.backref('session'))

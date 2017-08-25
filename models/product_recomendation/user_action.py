# -*- coding: utf-8 -*-

from datetime import datetime

from application import db


__all__ = [
    'UserAction'
]


class UserAction(db.Model):

    __tablename__ = 'user_action'

    ACTION_LIKE = 'like'
    ACTION_VIEW = 'view'

    AVAILABLE_ACTIONS = (ACTION_LIKE, ACTION_VIEW)

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.Integer, db.ForeignKey('user_session.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    action = db.Column(db.String(64), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'session': self.session.uid,
            'product': {'id': self.product.id, 'name': self.product.name},
            'action': self.action,
            'created_at': self.created_at.timestamp()
        }

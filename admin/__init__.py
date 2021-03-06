# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

import settings
from application import db

from . import views
from .models import User


__all__ = (
    'init_admin',
)


def init_admin(app):
    _init_login_manager(app)

    _create_admins()

    admin = Admin(
        app=app,
        index_view=views.AdminIndexView(name='Dressing room', url='/noadmin'),
        template_mode='bootstrap3'
    )

    import models
    model_names = models.__all__

    model_names.remove('Product')
    model_names.remove('Category')

    admin.add_view(views.ProductView(models.Product, session=db.session))
    admin.add_view(views.CategoryView(models.Category, session=db.session))

    [admin.add_view(views.ModelView(getattr(models, model_name), session=db.session))
     for model_name in model_names]

    return admin


def _init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def _create_admins():
    for login, password in settings.ADMINS:
        user = User.query.filter_by(login=login).first()
        if not user:
            user = User(login, generate_password_hash(password))
            db.session.add(user)

    db.session.commit()

# -*- coding: utf-8 -*-

import os

from urllib.parse import urljoin

import flask_admin
import flask_login

from flask_admin import expose, helpers
from flask_admin.form import ImageUploadField, ImageUploadInput
from flask_admin.contrib import sqla
from flask import redirect, url_for, request
from markupsafe import Markup

import settings

from admin.forms import LoginForm
from admin import utils
from admin.utils import get_photo_filename, get_photo_thumbname


class AdminIndexView(flask_admin.AdminIndexView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @expose('/')
    def index(self):
        from models.category import Category

        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        self._template_args['categories'] = Category.top_level()

        return super().index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            flask_login.login_user(user)

        if flask_login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form

        return super().index()

    @expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for('.index'))


class ModelView(sqla.ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class EasyUrlImageUploadInput(ImageUploadInput):

    def get_url(self, field):
        if field.thumbnail_size:
            filename = field.thumbnail_fn(field.data)
        else:
            filename = field.data
        return urljoin(field.url_relative_path, filename)


class EasyUrlImageUploadField(ImageUploadField):

    widget = EasyUrlImageUploadInput()


class ProductView(ModelView):

    DESCRIPTION_LIMIT = 70
    PHOTO_SIZE = 100
    UV_CARD_SIZE = 200

    def _description_formatter(self, context, model, name):
        return utils.ellipsis(model.description, self.DESCRIPTION_LIMIT)

    def _photo_formatter(self, context, model, name):
        return Markup('<img src="{}" width="{}">'.format(model.photo_url, self.PHOTO_SIZE))

    def _uv_card_formatter(self, context, model, name):
        return Markup('<img src="{}" width="{}">'.format(model.uv_card_url, self.UV_CARD_SIZE))

    def _url_formatter(self, context, model, name):
        return Markup('<a href="{}">Ссылка на товар</a>'.format(model.url))

    column_list = [
        'id',
        'name',
        'price',
        'photo',
        'uv_card',
        'url',
        'description',
        'gender',
        'is_childish',
        'category',
        'source'
    ]

    column_searchable_list = [
        'id', 'name'
    ]

    column_filters = [
        'id', 'category_id', 'gender', 'is_childish'
    ]

    column_formatters = {
        'description': _description_formatter,
        'photo': _photo_formatter,
        'url': _url_formatter,
        'uv_card': _uv_card_formatter
    }

    form_overrides = {
        'uv_card': EasyUrlImageUploadField,
        'photo': EasyUrlImageUploadField
    }

    form_args = {
        'photo': dict(
            base_path=os.path.join(settings.STATIC_PATH, 'images', 'products', 'photo'),
            namegen=get_photo_filename,
            thumbgen=get_photo_thumbname,
            allowed_extensions=('jpg', 'jpeg', 'png'),
            url_relative_path=urljoin(settings.STATIC_URL, 'products/')
        ),
        'uv_card': dict(
            base_path=os.path.join(settings.STATIC_PATH, 'images', 'products', 'uv_card'),
            namegen=get_photo_filename,
            thumbgen=get_photo_thumbname,
            allowed_extensions=('jpg', 'jpeg', 'png'),
            url_relative_path=urljoin(settings.STATIC_URL, 'uv_card/')
        ),
    }

    form_choices = {
        'gender': [
            ('male', 'Мужской'),
            ('female', 'Женский')
        ]
    }


class CategoryView(ModelView):

    form_choices = {
        'gender': [
            ('male', 'Мужской'),
            ('female', 'Женский')
        ],
        'skin_type': [
            ('00', 'Отсутствует'),
            ('01', 'Рубашка заправляемая'),
            ('02', 'Рубашка незаправляемая'),
            ('03', 'Джинсы с ремнём'),
            ('04', 'Джинсы без ремня'),
            ('05', 'Классические брюки'),
            ('06', 'Футболка'),
            ('07', 'Пиджак')
        ]
    }

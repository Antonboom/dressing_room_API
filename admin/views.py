# -*- coding: utf-8 -*-

import flask_admin
import flask_login

from flask_admin.contrib import sqla
from flask_admin import expose, helpers
from flask import redirect, url_for, request
from markupsafe import Markup

from admin.forms import LoginForm
from admin import utils


class AdminIndexView(flask_admin.AdminIndexView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))

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


class ProductView(ModelView):

    DESCRIPTION_LIMIT = 70
    PHOTO_SIZE = 100

    def _description_formatter(self, context, model, name):
        return utils.ellipsis(model.description, self.DESCRIPTION_LIMIT)

    def _photo_formatter(self, context, model, name):
        return Markup('<img src="{}" width="{}">'.format(model.photo, self.PHOTO_SIZE))

    def _url_formatter(self, context, model, name):
        return Markup('<a href="{}">Ссылка на товар</a>'.format(model.url))

    column_formatters = {
        'description': _description_formatter,
        'photo': _photo_formatter,
        'url': _url_formatter
    }

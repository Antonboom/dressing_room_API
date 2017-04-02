# -*- coding: utf-8 -*-

import flask_admin
import flask_login

from flask_admin.contrib import sqla
from flask_admin import expose, helpers
from flask import redirect, url_for, request

from admin.forms import LoginForm


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

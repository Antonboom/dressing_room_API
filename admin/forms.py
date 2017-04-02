# -*- coding: utf-8 -*-

from werkzeug.security import check_password_hash
from wtforms import form, fields, validators

from .models import User


class LoginForm(form.Form):

    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    INVALID_USER_MESSAGE = 'Invalid user'
    INVALID_PASSWORD_MESSAGE = 'Invalid password'

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError(self.INVALID_USER_MESSAGE)

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError(self.INVALID_PASSWORD_MESSAGE)

    def get_user(self):
        return User.query.filter_by(login=self.login.data).first()

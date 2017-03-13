# -*- coding: utf-8 -*-

from flask import Blueprint


api = Blueprint('api_v0', __name__)


@api.route('/')
def hello_world():
    return 'Hello from dressing room API'

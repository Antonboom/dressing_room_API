# -*- coding: utf-8 -*-

import os

# TODO: MAKE SECRET DATA TRULY SECRET

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = '/www/droom_backend/static'
STATIC_URL = 'http://cache.mydressing.ru/'

HOST = '0.0.0.0'
PORT = 8080

SECRET_KEY = ''

ADMINS = ()     # ((login, password),)

DEBUG = False


URL_ROOT_PREFIX = '/'      # for example /api, /other_prefix


MYSQL_HOST = 'localhost'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = 'droom_backend'

DB_TRACK_MODIFICATIONS = False


YANDEX_API_AUTH_TOKEN = 'vuD1vIbYy8Oufw0AcID1h1ySZ97YxL'


try:
    from local_settings import *

except ImportError:
    print('No local_settings')

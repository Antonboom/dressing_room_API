# -*- coding: utf-8 -*-

# TODO: MAKE SECRET DATA TRULY SECRET

HOST = '0.0.0.0'
PORT = 8080


DEBUG = False


URL_ROOT_PREFIX = '/'      # for example /api, /other_prefix


MYSQL_HOST = 'localhost'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = 'droom_backend'


YANDEX_API_AUTH_TOKEN = 'vuD1vIbYy8Oufw0AcID1h1ySZ97YxL'


try:
    from local_setting import *

except ImportError:
    pass

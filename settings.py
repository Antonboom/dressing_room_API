# -*- coding: utf-8 -*-

host = '0.0.0.0'
port = 8080

debug = False

# url_root = '/api'
url_root = '/'


try:
    from local_setting import *

except ImportError:
    pass

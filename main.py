# -*- coding: utf-8 -*-

import settings

from urllib.parse import urljoin
from flask import Flask
from api.v0.handlers import api as api_v0


def _get_url_prefix(version_num=0):
    return urljoin(settings.url_root, 'v{}'.format(version_num))


app = Flask(__name__)
app.register_blueprint(api_v0, url_prefix=_get_url_prefix())


def main():
    app.run(host=settings.host, port=settings.port, debug=settings.debug)


def gunicorn():
    return app


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

import settings

from urllib.parse import urljoin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.v0.handlers import api as api_v0


__all__ = (
    'db',
)


def _get_url_prefix(version_num=0):
    return urljoin(settings.URL_ROOT_PREFIX, 'v{}'.format(version_num))


def _get_sql_alchemy_db_uri():
    return 'mysql://{username}:{password}@{host}/{dbname}'.format(
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        dbname=settings.MYSQL_DB
    )


app = Flask(__name__)
app.register_blueprint(api_v0, url_prefix=_get_url_prefix())

app.config['SQLALCHEMY_DATABASE_URI'] = _get_sql_alchemy_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.DB_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

import models               # Oh my God...

migrate = Migrate(app, db)


def main():
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


def gunicorn():
    return app


if __name__ == '__main__':
    main()

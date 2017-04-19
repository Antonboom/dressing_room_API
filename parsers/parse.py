# -*- coding: utf-8 -*-

import traceback

from application import db
from models import Category, Source
from parsers.lamoda_parser import LamodaCategoryParser


PAGES_COUNT = 1


def _get_or_create_lamoda_source():
    source = Source.query.filter_by(name='lamoda.ru').first()

    if source is None:
        source = Source(
            name='lamoda.ru',
            site_url='http://www.lamoda.ru/',
            logo_url='http://www.lamoda.ru/social-logo.jpg',
            is_active=True
        )

        db.session.add(source)
        db.session.commit()

    return source


source = _get_or_create_lamoda_source()
category = Category.query.get(11)

products = LamodaCategoryParser(category=category, source=source).get_products()

for product in products:
    try:
        db.session.add(product)
        db.session.commit()

    except Exception as exception:
        db.session.rollback()
        print('Received top level error: ', exception, traceback.format_exc())

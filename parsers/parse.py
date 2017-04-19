# -*- coding: utf-8 -*-

from application import db
from models import Category, Source
from parsers.lamoda_parser import LamodaCategoryParser

PAGES_COUNT = 1

source = Source.query.filter_by(name='lamoda.ru').first()
category = Category.query.get(11)

products = LamodaCategoryParser(category=category, source=source).get_products()

for product in products:
    try:
        db.session.add(product)
        db.session.commit()

    except Exception as exception:
        db.session.rollback()
        print('LOL', exception)

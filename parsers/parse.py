# -*- coding: utf-8 -*-

import traceback
import sys
import logging

sys.path.append('.')

import settings
from application import db
from models import Category, Source
from parsers.lamoda_parser import LamodaCategoryParser


PAGES_COUNT = 10


logger = logging.getLogger(__name__)


def _setup_logging():
    log_handler = logging.FileHandler(settings.PARSING_LOG_FILE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s\t%(message)s', '%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(formatter)
    logging.root.addHandler(log_handler)
    logging.root.setLevel(logging.INFO)


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


def lamoda_parsing():
    source = _get_or_create_lamoda_source()
    categories = Category.query.filter(Category.parent_id.notin_([0, 1000])).all()

    for category in categories:
        logging.info('Parsing category {}'.format(category))

        for page in range(1, PAGES_COUNT + 1):
            products = LamodaCategoryParser(category=category, source=source).get_products(page)

            product_count = 0

            for product in products:
                try:
                    db.session.add(product)
                    db.session.commit()

                    logger.info('New product {} added'.format(product))
                    product_count += 1
                    print('.', end='')

                except Exception as exception:
                    db.session.rollback()
                    logger.error('{}: Received parsing top level error: {}'.format(category, exception))

            logger.info('\nFor category "{}" received {} products!'.format(category.name, product_count))


if __name__ == '__main__':
    _setup_logging()
    lamoda_parsing()

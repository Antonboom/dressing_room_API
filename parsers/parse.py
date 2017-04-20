# -*- coding: utf-8 -*-

import sys
import logging

sys.path.append('.')

from sqlalchemy.sql.elements import and_

import settings

from application import db
from models import Category, Source
from parsers.lamoda_parser import LamodaCategoryParser


PAGES_COUNT = 3


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


def retry(n):
    def decorator(func):
        def wrapper(*fargs, **fkwargs):
            for i in range(n):
                try:
                    value = func(*fargs, **fkwargs)
                    return value

                except Exception:
                    logging.warning('Try {} №{}'.format(func.__name__, i))
                    pass
        return wrapper
    return decorator


@retry(20)
def lamoda_parsing():
    source = _get_or_create_lamoda_source()
    categories = Category.query.filter(and_(Category.parent_id.notin_([0, 10, 20, 30, 40, 50]), Category.id.notin_([]))).all()

    for category in categories:
        logging.info('Parsing category {}'.format(category))

        parser = LamodaCategoryParser(category=category, source=source)
        for page in range(1, PAGES_COUNT + 1):
            products = parser.get_products(page)

            product_count = 0

            for product in products:
                try:
                    db.session.add(product)
                    db.session.commit()

                    logger.info('New product {} added'.format(product))
                    product_count += 1

                except Exception as exception:
                    db.session.rollback()
                    logger.error('{}: Received parsing top level error: {}'.format(category, exception))

            logger.info('For category "{}" received {} products!'.format(category, product_count))


if __name__ == '__main__':
    _setup_logging()
    lamoda_parsing()

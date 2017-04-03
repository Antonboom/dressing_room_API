# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append('.')

from application import db
from models import Category


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIES_DATA_PATH = os.path.join(PROJECT_DIR, 'data', 'categories.json')


def init_categories():
    categories_deleted_number = Category.query.delete()
    db.session.commit()

    print('{} categories deleted'.format(categories_deleted_number))

    categories = json.load(open(CATEGORIES_DATA_PATH))
    for category_data in categories:
        db.session.add(
            Category(**category_data)
        )

    db.session.commit()

    print('{} categories created'.format(len(categories)))


if __name__ == '__main__':
    try:
        init_categories()

    except Exception as exception:
        print('Init categories failed, because of {}'.format(exception))

# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append('.')

import settings

from application import db
from models import Color


COLORS_DATA_PATH = os.path.join(settings.PROJECT_DIR, 'data', 'colors.json')


def init_colors():
    colors_deleted_number = Color.query.delete()
    db.session.commit()

    print('{} colors deleted'.format(colors_deleted_number))

    colors = json.load(open(COLORS_DATA_PATH))
    for color_data in colors:
        db.session.add(
            Color(**color_data)
        )

    db.session.commit()

    print('{} colors created'.format(len(colors)))


if __name__ == '__main__':
    try:
        init_colors()

    except Exception as exception:
        print('Init colors failed, because of {}'.format(exception))

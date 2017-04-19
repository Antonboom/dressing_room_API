# -*- coding: utf-8 -*-

import sys

sys.path.append('.')

from application import db
from models import Category, Size


# https://www.kupivip.ru/info/razmery
# chest - грудь, waist - талия, hip - бедро


tables = (
    # Женское
    # Блузки, туники, куртки, платья
    {
        'size': 17,
        'table': {
            'chest_girth':   [size for size in range(76, 144, 4)],
            'waist_girth':   [size for size in range(58, 124, 4)],
            'hip_girth':     [82, 86] + [size for size in range(92, 152, 4)],
            'sleeve_length': [58, 59, 59, 60, 60, 60, 61, 61, 61, 61, 62, 62,  62.5, 62.5, 62.5, 62.5, 62.5],
            'russia':        [size for size in range(38, 72, 2)],
            'europe':        [size for size in range(32, 66, 2)],
            'uk':            [size for size in range(4, 38, 2)],
            'usa':           [size for size in range(0, 34, 2)],
            'international': ['XXS', 'XS', 'S', 'M', 'M', 'L', 'L', 'XL', 'XXL', 'XXL', 'XXXL', '4XL', '4XL', '4XL', '5XL', '5XL', '5XL']
        },
        'categories': ()
    },

    # Брюки, юбки, шорты
    {
        'size': 17,
        'table': {
            'waist_girth':   [58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 100, 104, 108, 112, 116, 120],
            'hip_girth':     [82, 86] + [size for size in range(92, 152, 4)],
            'russia':        [size for size in range(38, 72, 2)],
            'europe':        [size for size in range(32, 66, 2)],
            'uk':            [size for size in range(4, 38, 2)],
            'usa':           [size for size in range(0, 34, 2)],
            'international': ['XXS', 'XS', 'S', 'M', 'M', 'L', 'L', 'XL', 'XXL', 'XXL', 'XXXL', '4XL', '4XL', '4XL', '5XL', '5XL', '5XL']
        },
        'categories': ()
    },

    # Джинсы
    {
        'size': 15,
        'table': {
            'waist_girth':   [size for size in range(58, 102, 4)] + [100, 104, 108, 112],
            'hip_girth':     [82, 86] + [size for size in range(92, 144, 4)],
            'russia':        [38] + [size for size in range(42, 68, 2)],
            'usa':           [size for size in range(0, 32, 2)],
            'international': ['XXS', 'XS', 'S', 'M', 'M', 'L', 'L', 'XL', 'XLL', 'XXL', 'XXXL', '4XL', '4XL', '4XL', '5XL']
        },
        'categories': ()
    },

    # Нижнее белье
    {
        'size': 17,
        'table': {
            'waist_girth':   [58, 62, 65, 68, 74, 78, 82, 85, 88, 92, 97, 101, 106,  110,  114,  118,  122],
            'hip_girth':     [82, 86] + [size for size in range(92, 152, 4)],
            'russia':        [size for size in range(38, 72, 2)],
            'europe':        [size for size in range(32, 66, 2)],
            'uk':            [size for size in range(4, 38, 2)],
            'usa':           [size for size in range(0, 34, 2)],
            'international': ['XXS', 'XS', 'S', 'M', 'M', 'L', 'L', 'XL', 'XL', 'XXL', 'XXXL', 'XXXL', 'XXXL', 'XXXL', 'XXXL', 'XXXL', 'XXXL']
        },
        'categories': ()
    },

    # Мужское
    # Пиджаки, джемперы, жилеты, халаты, свитеры, куртки, рубашки
    {
        'size': 14,
        'table': {
            'chest_girth':   [size for size in range(88, 144, 4)],
            'waist_girth':   [size for size in range(70, 124, 6)] + [size for size in range(120, 140, 4)],
            'hip_girth':     [size for size in range(92, 136, 4)] + [134, 136, 138],
            'sleeve_length': [59, 60, 61, 62, 63, 63, 64, 64, 65, 65, 66, 66, 66, 66],
            'russia':        [size for size in range(44, 72, 2)],
            'europe':        [size for size in range(38, 66, 2)],
            'uk':            [size for size in range(32, 56, 2)] + [60, 62],
            'usa':           [size for size in range(34, 56, 2)] + [60, 62, 64],
            'international': ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXL', 'XXXL', '4XL', '4XL', '5XL', '5XL']
        },
        'categories': (20, 21, 22, 30, 31, 32, 33, 50, 51, 52, 80, 81, 82, 83, 90, 91, 92, 93, 94, 100, 101, 102, 103, 104)
    },

    # Брюки, шорты
    {
        'size': 14,
        'table': {
            'waist_girth':   [size for size in range(70, 124, 6)] + [size for size in range(120, 140, 4)],
            'hip_girth':     [size for size in range(92, 136, 4)] + [134, 136, 138],
            'russia':        [size for size in range(44, 72, 2)],
            'europe':        [size for size in range(38, 66, 2)],
            'uk':            [size for size in range(32, 56, 2)] + [60, 62],
            'usa':           [size for size in range(34, 56, 2)] + [60, 62, 64],
            'international': ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXL', 'XXXL', '4XL', '4XL', '5XL', '5XL']
        },
        'categories': (10, 11, 12, 13, 72, 110, 111, 112, 113, 114)
    },

    # Джинсы
    {
        'size': 10,
        'table': {
            'waist_girth':   [size for size in range(70, 124, 6)] + [size for size in range(120, 140, 4)],
            'hip_girth':     [size for size in range(92, 136, 4)] + [134, 136, 138],
            'russia':        [size for size in range(44, 72, 2)],
            'usa':           [size for size in range(4, 24, 2)],
            'international': ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXL', 'XXXL']
        },
        'categories': (40, 41, 42)
    },

    # Нижнее белье
    {
        'size': 14,
        'table': {
            'waist_girth':   [78, 82] + [size for size in range(84, 132, 4)],
            'hip_girth':     [size + 0.6 for size in range(95, 137, 3)],
            'russia':        [size for size in range(44, 72, 2)],
            'europe':        [size for size in range(38, 66, 2)],
            'uk':            [36, 38, 40, 42] + [size for size in range(42, 62, 2)],
            'usa':           [36, 38, 40, 42] + [size for size in range(42, 62, 2)],
            'international': ['S', 'S', 'M', 'M', 'L', 'L', 'XL', 'XL', 'XXL', 'XXL', 'XXXL', 'XXXL', 'XXXL', 'XXXL']
        },
        'categories': (60, 61, 62, 70, 71)
    },
)


def _print_table(number=None):
    def _print(table_data):
        table = table_data['table']
        size = table_data['size']

        print(
            ('{:<15}' * 9).format(
                'Россия', 'Международ', 'Грудь', 'Талия', 'Бедра', 'Рукав', 'Англия', 'США', 'Европа')
        )

        [
            print(
                ('{:<15}' * 9).format(
                    table['russia'][row],
                    table['international'][row],
                    table.get('chest_girth', ['-'] * size)[row],
                    table['waist_girth'][row],
                    table['hip_girth'][row],
                    table.get('sleeve_length', ['-'] * size)[row],
                    table.get('uk', ['-'] * size)[row],
                    table['usa'][row],
                    table.get('europe', ['-'] * size)[row],
                )
            )
            for row in range(size)
        ]

    if number:
        _print(tables[number])
    else:
        for table_data in tables:
            print('*' * 100)
            _print(table_data)


def init_sizes():
    for table_data in tables:
        table_size = table_data['size']
        table = table_data['table']

        categories = table_data['categories']

        sizes_count = 0

        if categories:
            sizes = [{name: sizes[row] for name, sizes in table.items()} for row in range(table_size)]

            for category_id in categories:
                category = Category.query.get(category_id)

                for size_data in sizes:
                    size = Size(**size_data)
                    db.session.add(size)
                    category.sizes.append(size)

            sizes_count += len(sizes) * len(categories)

    db.session.commit()

    print('{} sizes created'.format(sizes_count))


if __name__ == '__main__':
    try:
        init_sizes()

    except Exception as exception:
        print('Init sizes failed, because of {}'.format(exception))

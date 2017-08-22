# -*- coding: utf-8 -*-

from .category import Category
from .color import Color
from .product import Product
from .source import Source
from .size import Size

from . import colors_recomendation
from .colors_recomendation import *


__all__ = [
    'Source',
    'Category',
    'Product',
    'Color',
    'Size',
]

__all__ += colors_recomendation.__all__

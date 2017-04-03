# -*- coding: utf-8 -*-

import models

from flask import Blueprint

from api import JsonResponse


api = Blueprint('api_v0', __name__)


@api.route('/', methods=('GET',))
def hello_from_API():
    return 'Hello from dressing room API'


@api.route('/categories', methods=('GET',))
def get_categories():
    categories = models.Category.query.filter_by(parent_id=None).all()
    return JsonResponse([category.serialize() for category in categories])


@api.route('/categories/<int:category_id>', methods=('GET',))
def get_category(category_id):
    category = models.Category.query.get(category_id)
    return JsonResponse(category.serialize())

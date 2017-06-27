# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    request,
)

from sqlalchemy.sql.elements import and_

import models as m
from api import JsonResponse

api = Blueprint('api_v0', __name__)


def _json_list(serializable_sequence, full=False):
    return JsonResponse([item.full_serialize() if full else item.serialize() for item in serializable_sequence])


def _make_error(message):
    return {'error': message}


@api.route('/', methods=('GET',))
def hello_from_api():
    return 'OK'


@api.route('/category/<int:category_id>', methods=('GET',))
def get_category(category_id):
    category = m.Category.query.get(category_id)

    if category is None:
        return JsonResponse(_make_error('Category not found'), status=404)

    return JsonResponse(category.serialize())


@api.route('/categories', methods=('GET',))
def get_categories():
    genders = ('male', 'female')

    gender = request.args.get('gender')
    if gender not in genders:
        return JsonResponse(_make_error('No gender specified'), status=400)

    categories = m.Category.query.filter(and_(m.Category.parent_id.is_(None), m.Category.gender == gender)).all()
    return _json_list(categories)


@api.route('/category/<int:category_id>/children', methods=('GET',))
def get_category_childrens(category_id):
    category = m.Category.query.get(category_id)

    if category is None:
        return JsonResponse(_make_error('Category not found'), status=404)

    childrens = m.Category.query.filter_by(parent_id=category_id).all()
    return _json_list(childrens)


@api.route('/category/<int:category_id>/sizes', methods=('GET',))
def get_category_sizes(category_id):
    category = m.Category.query.get(category_id)

    if category is None:
        return JsonResponse(_make_error('Category not found'), status=404)

    return _json_list(category.sizes)


@api.route('/category/<int:category_id>/products', methods=('GET',))
def get_category_products(category_id):
    category = m.Category.query.get(category_id)

    if category is None:
        return JsonResponse(_make_error('Category not found'), status=404)

    results_per_page = int(request.args.get('results_per_page', 30))
    page = int(request.args.get('page', 1))

    products = category.products[results_per_page * page: results_per_page * (page + 1)]

    response = {
        'page': page,
        'count': len(products),
        'products': [product.serialize() for product in products]
    }

    return JsonResponse(response)


@api.route('/product/<int:product_id>', methods=('GET',))
def get_product(product_id):
    product = m.Product.query.get(product_id)

    if product is None:
        return JsonResponse(_make_error('Product not found'), status=404)

    return JsonResponse(product.full_serialize())


@api.route('/size/<int:size_id>', methods=('GET',))
def get_size(size_id):
    size = m.Size.query.get(size_id)

    if size is None:
        return JsonResponse(_make_error('Size not found'), status=404)

    return JsonResponse(size.full_serialize())


@api.route('/uv_card', methods=('GET',))
def get_uvcard():
    pid = request.args.get('pid', []).split(',')
    return 'ok'
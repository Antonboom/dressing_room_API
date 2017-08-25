# -*- coding: utf-8 -*-

import random

from flask import (
    Blueprint,
    request,
    make_response
)
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import and_

import models as m

from application import db
from api import JsonResponse
from uv_card.processing import (
    UVcardPart,
    UVcard
)


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
    gender = request.args.get('gender')
    if gender not in m.Product.GENDERS:
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
    with_uv_card = bool(request.args.get('with_uv_card', False))

    products = category.products
    if with_uv_card:
        products = list(filter(lambda product: product.uv_card, category.products))

    products = products[results_per_page * (page - 1): results_per_page * page]

    response = {
        'page': page,
        'count': len(products),
        'products': [product.serialize() for product in products]
    }

    return JsonResponse(response)


@api.route('/products', methods=('GET',))
def get_products():
    gender = request.args.get('gender', None)
    results_per_page = int(request.args.get('results_per_page', 30))
    page = int(request.args.get('page', 1))
    get_all = bool(request.args.get('all', False))

    _filter = m.Product.uv_card.isnot(None)
    if gender:
        _filter = and_(_filter, m.Product.gender == gender)

    if get_all:
        products = m.Product.query.filter(_filter).all()
    else:
        products = m.Product.query.filter(_filter).limit(results_per_page).offset(results_per_page * (page - 1)).all()

    response = {
        'products': [product.full_serialize() for product in products],
        'count': len(products)
    }

    if not get_all:
        response['page'] = page

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
    pid = request.args.get('pid', '')

    if not pid:
        return JsonResponse(_make_error('No "pid" argument'), status=400)

    pid = pid.split(',')

    # categories: (width, height, left, top)
    categories_part_params_map = {
        (10, 40, 60, 70, 110):     (450, 669, 0, 355),  # Нижняя одежда
        (20, 30, 50, 80, 90, 100): (1024, 355, 0, 0),   # Верхняя одежда
    }

    parts = []

    for product_id in pid:
        product = m.Product.query.get(product_id)

        if product is None:
            return JsonResponse(_make_error('Product with id="{}" not found'.format(product_id)), status=404)

        category = product.category
        while category.parent:
            category = category.parent

        params = None
        for categories, part_params in categories_part_params_map.items():
            if category.id in categories:
                params = part_params
                continue

        if params is None:
            return JsonResponse(_make_error('No part params for category with id="{}"'.format(category.id)), status=404)

        if not product.uv_card_path:
            return JsonResponse(_make_error('No uv-card for product with id="{}"'.format(product_id)), status=404)

        parts.append(UVcardPart(product.uv_card_path, *params))

    card = UVcard(*parts)
    response = make_response(card.make_blob())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@api.route('/fashion', methods=('GET',))
def get_fashion():
    pid = request.args.get('pid', '')

    if not pid:
        return JsonResponse(_make_error('No "pid" argument'), status=400)

    pids = pid.split(',')

    current_seasons = m.FashionSeason.query.filter(m.FashionSeason.is_active.is_(True)).all()
    suitable_seasons = []

    for season in current_seasons:
        percent = season.get_compatibility_percentage(pids)
        if percent:
            suitable_seasons.append({
                'season': season.serialize(pids),
                'compatibility': percent
            })

    return JsonResponse(suitable_seasons)


@api.route('/recommendation/auth', methods=('GET',))
def get_user_session():
    user_session = m.UserSession()

    db.session.add(user_session)
    db.session.commit()

    return JsonResponse({'session': user_session.uid})


@api.route('/recommendation/action', methods=('POST',))
def send_user_action():
    post_data = request.get_json() or {}

    session_id = post_data.get('session')
    if not session_id:
        return JsonResponse(_make_error('No "session" specified'), status=400)

    product_id = int(post_data.get('product', 0))
    if not product_id:
        return JsonResponse(_make_error('No "product" specified'), status=400)

    action = post_data.get('action')
    if not action:
        return JsonResponse(_make_error('No "action" specified'), status=400)
    if action not in m.UserAction.AVAILABLE_ACTIONS:
        return JsonResponse(_make_error('Available actions: {}'.format(m.UserAction.AVAILABLE_ACTIONS)), status=400)

    session = m.UserSession.query.filter_by(uid=session_id).first()
    if session is None:
        return JsonResponse(_make_error('Session "{}" not found'.format(session_id)), status=404)

    product = m.Product.query.get(product_id)
    if product is None:
        return JsonResponse(_make_error('Product with id="{}" not found'.format(product_id)), status=404)

    user_action = m.UserAction(session_id=session.id, product_id=product_id, action=action)
    db.session.add(user_action)
    db.session.commit()

    return JsonResponse(user_action.serialize())


@api.route('/recommendation', methods=('GET',))
def get_recommendation():
    session_uid = request.args.get('session', '')

    if not session_uid:
        return JsonResponse(_make_error('No "session" argument'), status=400)

    default_products_count = 10
    products_count = int(request.args.get('count', default_products_count))

    actions = m.UserAction.query.join(m.UserSession)\
        .options(joinedload(m.UserAction.product))\
        .filter(and_(m.UserAction.action == m.UserAction.ACTION_VIEW, m.UserSession.uid == session_uid))\
        .order_by(desc(m.UserAction.created_at))\
        .limit(products_count)\
        .all()

    categories = [action.product.category_id for action in actions]
    categories_count = len(categories)

    categories_percentage = {}
    for category_id in categories:
        if category_id not in categories_percentage:
            categories_percentage[category_id] = round(categories.count(category_id) / categories_count, 4)

    categories_percentage = sorted(categories_percentage.items(), key=lambda item: -item[1])

    categories_products_count = {}
    tmp_products_count = products_count
    for category_id, percent in categories_percentage:
        count = percent * products_count

        if count:
            count = 1 if 0 < count < 0.1 else int(count)

            categories_products_count[category_id] = count
            tmp_products_count -= count
            if tmp_products_count <= 0:
                break
        else:
            break

    products = []
    for category_id, count in categories_products_count.items():
        # TODO: Разгрузить БД
        category_products = m.Category.query.get(category_id).products
        products.extend(random.choice(category_products) for _ in range(count))

    resulting_count = len(products)
    if resulting_count < products_count:
        products.extend([
            # TODO: Разгрузить БД, убрать магические числа
            random.choice(m.Product.query.limit(1000).offset(random.choice(2000)).all())
            for _ in range(products_count - resulting_count)
        ])

    return JsonResponse({
        'session': session_uid,
        'products': [product.serialize() for product in products]
    })

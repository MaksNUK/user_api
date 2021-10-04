from connexion import NoContent
from flask import request

from app.models.db_api_user import UserDBAPI


def create(user: UserDBAPI):
    title = request.form.get('title')
    if title:
        user = user.product_list.create(title=title)
        if user:
            return user, 201
    return NoContent, 204


def read(user: UserDBAPI):
    result = user.product_list.read_all()
    if result:
        return {'result': result}
    return NoContent, 204


def delete(user: UserDBAPI):
    products_list_id = request.form.get('products_list_id')

    if products_list_id:
        result = user.product_list.delete_list(
            products_list_id=products_list_id
        )
        return {'result': result}
    return NoContent, 204


def add_product(user: UserDBAPI):
    product_id = request.form.get('product_id')
    products_list_id = request.form.get('products_list_id')

    if product_id:
        result = user.product_list.add_product(
            product_id=product_id,
            products_list_id=products_list_id
        )
        return {'result': result}
    return NoContent, 204


def delete_product(user: UserDBAPI):
    product_id = request.form.get('product_id')
    products_list_id = request.form.get('products_list_id')

    if product_id:
        user = user.product_list.delete_product(
            product_id=product_id,
            products_list_id=products_list_id
        )
        if user:
            return user, 201
    return NoContent, 204


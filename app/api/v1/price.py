from connexion import NoContent
from flask import request

from app.models.db_api_price import PriceDBAPI

price_api = PriceDBAPI()


def get(id_):
    result = price_api.get(id_=id_)
    if result:
        return result, 200
    return NoContent, 204


def update():
    body_json = request.json
    product_id = body_json.get('product_id')
    currency_id = body_json.get('currency_id')
    price = body_json.get('price')

    result = price_api.update(
        product_id=product_id,
        currency_id=currency_id,
        price=price
    )
    if result:
        return {'result': result}, 201
    return NoContent, 204

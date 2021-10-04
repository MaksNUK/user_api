from connexion import NoContent
from flask import request

from app.models.db_api_currency import CurrenciesDBAPI

currency_api = CurrenciesDBAPI()


def read_all(sort: str = None, page: int = 1, page_size: int = 5):
    """Get currencies list."""
    currencies = currency_api.get(
        sort=sort,
        offset=page-1,
        page_size=page_size,
    )
    if currencies and isinstance(currencies, list):
        return currencies, 200
    if isinstance(currencies, dict):
        return currencies, 500
    return NoContent, 204


def add():
    """Create currency."""
    title = request.form.get('title')
    if title:
        title = title.upper()
        currency = currency_api.add(title=title)
        if currency:
            if 'currency_id' in currency:
                return currency, 201
            if 'duplicate' in currency:
                return currency, 200
            if isinstance(currency, dict):
                return currency, 500
    return NoContent, 204


def delete(id_):
    """Delete currency."""
    result = currency_api.delete(id_=id_)
    if result:
        if 'deleted' in result:
            return result, 200
    return NoContent, 204

from sqlalchemy import and_
from sqlalchemy.dialects.mysql import insert

from app.models.mysql_tables import Currencies, currency_and_product, session


class PriceDBAPI:
    def __init__(self):
        self.session = session

    @staticmethod
    def update(product_id, currency_id, price):
        with session() as s:
            currency = insert(currency_and_product).values(
                product_id=product_id,
                currency_id=currency_id,
                price=price,
            )
            on_duplicate_currency = currency.on_duplicate_key_update(
                product_id=product_id,
                currency_id=currency_id,
                price=price
            )
            s.execute(on_duplicate_currency)
            s.commit()
            if s.query(currency_and_product).filter(and_(
                currency_and_product.columns.product_id == product_id,
                currency_and_product.columns.currency_id == currency_id
            )):
                return True
            return False

    @staticmethod
    def get(id_):
        with session() as s:
            prices = (s.query(Currencies, currency_and_product.columns.price)
                      .join(currency_and_product)
                      .filter(currency_and_product.columns.product_id == id_)
                      .all())
            product_prices = dict()
            for currency, price in prices:
                if currency.title and price:
                    product_prices.update({currency.title: price})
            return product_prices

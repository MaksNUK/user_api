from app.models.mysql_tables import session, Users, Currencies


class CurrenciesDBAPI:
    def __init__(self):
        self.session = session

    def get(self, sort=None, offset=0, page_size=5):
        """

        :param str sort: 'acs' or 'desc'
        :param int page_size: Results on page
        :param int offset: Page
        :returns: Return user info
        """
        with self.session() as s:
            try:
                currencies = s.query(Currencies)
                if sort == 'asc':
                    currencies = currencies.order_by(Currencies.title.asc())
                if sort == 'desc':
                    currencies = currencies.order_by(Currencies.title.desc())
                currencies = (currencies
                              .limit(page_size)
                              .offset(offset * page_size)
                              .all())
                if currencies:
                    currencies = [_.__dict__ for _ in currencies]
                    [_.pop('_sa_instance_state') for _ in currencies]
                    return currencies
                return []
            except Exception as e:
                return {"error": e.__str__()}

    def add(self, title: str):
        with self.session() as s:
            try:
                currency = Currencies(title)
                s.add(currency)
                s.commit()
                return {'currency_id': currency.id}
            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                if 'Duplicate' in e.__str__():
                    return {'duplicate': 'Value not unique'}
                return {"error": e.__str__()}

    def delete(self, id_):
        with self.session() as s:
            try:
                currency = s.query(Currencies).filter(Currencies.id == id_)
                if not currency.first():
                    return None
                if currency:
                    currency.delete()
                    s.commit()
                if not currency.first():
                    return {'deleted': True}
            except Exception as e:
                return {"error": e.__str__()}

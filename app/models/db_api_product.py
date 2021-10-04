from app.models.mysql_tables import session, Products, Users


class ProductDBAPI:
    def __init__(self):
        self.session = session

    def add(self, user: dict):
        with self.session() as s:
            try:
                new_product = Products(**user)
                s.add(new_product)
                s.commit()
                return {'user_id': new_product.id}

            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    @staticmethod
    def image(id_, new_info):
        with session() as s:
            try:
                product = s.query(Products).filter(Products.id == id_)
                update = product.first()
                if new_info.get('image') and update:
                    update.image = new_info.get('image')
                else:
                    update.image = update.image
                s.commit()
                return {'image': product.first().image}
            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    @staticmethod
    def get_image(id_):
        with session() as s:
            product = s.query(Products).filter(Products.id == id_).first()
            if product:
                return product.image

    def read_all(self, sort=None, offset=0, page_size=5):
        """

        :param str sort: Optional value ['acs', 'desc']
        :param int page_size: Results on page
        :param int offset: Page
        :rtype Union[list, Dict[str, str], Dict[str, str]]:
        :returns: Return user info
        """
        with self.session() as s:
            try:
                products = s.query(Products)
                if sort == 'asc':
                    products = products.order_by(Products.id.asc())
                if sort == 'desc':
                    products = products.order_by(Products.id.desc())
                products = (products
                            .limit(page_size)
                            .offset(offset * page_size)
                            .all())
                if products:
                    products = [_.__dict__ for _ in products]
                    [_.pop('_sa_instance_state') for _ in products]
                    return products
                return []

            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    def delete(self, id_):
        with self.session() as s:
            try:
                product = s.query(Products).filter(Products.id == id_)
                if product:
                    product.delete()
                    s.commit()
                else:
                    return {'product': 'Not found'}
                if not product.first():
                    return {'product': 'Product deleted'}
            except Exception as e:
                return {"error": e.__str__()}

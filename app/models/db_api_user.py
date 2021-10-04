from sqlalchemy import and_

from app.models.mysql_tables import session, Users, ProductsLists, \
    product_and_products_lists


class UserDBAPI:
    def __init__(self, id_=None):
        self.id_ = id_
        self.session = session
        self.product_list = self.ProductListDBAPI(id_=id_)

    def avatar(self):
        with session() as s:
            user = s.query(Users.avatar).filter(Users.id == self.id_).first()
            if user.avatar:
                return user.avatar
            return None

    def get(self, sort=None, offset=0, page_size=5):
        """

        :param str sort: Optional value ['acs', 'desc']
        :param int page_size: Results on page
        :param int offset: Page
        :rtype Union[list, Dict[str, str], Dict[str, str]]:
        :returns: Return user info
        """
        with self.session() as s:
            try:
                if self.id_:
                    user = s.query(Users).filter(Users.id == self.id_).first()
                    if user:
                        user = user.__dict__
                        user.pop('_sa_instance_state')
                    return user

                users = s.query(Users)
                if sort == 'asc':
                    users = users.order_by(Users.id.asc())
                if sort == 'desc':
                    users = users.order_by(Users.id.desc())
                users = users.limit(page_size).offset(offset * page_size).all()
                if users:
                    users = [_.__dict__ for _ in users]
                    [_.pop('_sa_instance_state') for _ in users]
                    return users
                return []

            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    def add(self, user: dict):
        with self.session() as s:
            try:
                new_user = Users(**user)
                s.add(new_user)
                s.commit()
                return {'user_id': new_user.id}

            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    def update(self, new_info) -> dict:
        """

        :param dict new_info: Dict with optional keys [avatar, name]
        :return: updated user info
        """
        with self.session() as s:
            try:
                user = s.query(Users).filter(Users.id == self.id_)
                update = user.first()
                update.avatar = new_info.get('avatar') if new_info.get(
                    'avatar') else update.avatar
                update.name = new_info.get('name') if new_info.get(
                    'name') else update.name
                s.commit()
                user_updated = dict(user.first().__dict__)
                [user_updated.pop(key) for key in tuple(user_updated.keys())
                 if key.startswith('_')]
                return user_updated
            except TypeError as e:
                return {"error": e.__str__().lstrip('__init__() ')}
            except Exception as e:
                return {"error": e.__str__()}

    def delete(self, id_):
        """Delete user."""
        with self.session() as s:
            try:
                user = s.query(Users).filter(Users.id == id_)
                if not user.first():
                    return None
                if user:
                    user.delete()
                    s.commit()
                if not user.first():
                    return {'deleted': True}
            except Exception as e:
                return {"error": e.__str__()}

    class ProductListDBAPI:
        def __init__(self, id_):
            self.id_ = id_

        def create(self, title):
            with session() as s:
                products_list = ProductsLists(user_id=self.id_, title=title)
                s.add(products_list)
                s.commit()
                return {'products_list_id': products_list.id}

        def read_all(self, sort=None, offset=0, page_size=5):
            with session() as s:
                products_lists = s.query(ProductsLists).filter(
                    ProductsLists.user_id == self.id_)
                if sort == 'asc':
                    products_lists = products_lists.order_by(
                        ProductsLists.id.asc())
                if sort == 'desc':
                    products_lists = products_lists.order_by(
                        ProductsLists.id.desc())
                products_lists = (products_lists
                                  .limit(page_size)
                                  .offset(offset * page_size)
                                  .all())
                if products_lists:
                    products = [_.__dict__ for _ in products_lists]
                    [_.pop('_sa_instance_state') for _ in products]
                    return products
                return []

        def delete_list(self, products_list_id):
            with session() as s:
                result = s.query(ProductsLists).filter(and_(
                    ProductsLists.user_id == self.id_,
                    ProductsLists.id == products_list_id,
                )).delete()
                s.commit()
                if result:
                    return True
                return False

        @staticmethod
        def add_product(product_id, products_list_id):
            with session() as s:
                product = product_and_products_lists.insert().values(
                    product_id=product_id,
                    products_list_id=products_list_id,
                )
                s.execute(product)
                s.commit()
                if s.query(product_and_products_lists).filter(and_(
                        product_and_products_lists.columns.product_id == product_id,
                        product_and_products_lists.columns.products_list_id == products_list_id
                )):
                    return True
                return False

        @staticmethod
        def delete_product(product_id, products_list_id):
            with session() as s:
                product = s.query(product_and_products_lists).filter_by(
                    product_id=product_id,
                    products_list_id=products_list_id,
                ).delete()
                s.commit()
                if product:
                    return True
                return False

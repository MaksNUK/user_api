import os
from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    ForeignKey,
    Float,
    PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

Base = declarative_base()
host = f"{'db' if os.getenv('DOCKER') == 'docker' else 'localhost'}"
engine = create_engine(f'mysql://root:secretpassword@{host}:3306/user_api_db')


@contextmanager
def session():
    connection = engine.connect()
    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine
        )
    )
    try:
        yield db_session
    except TypeError as e:
        return {"error": e.__str__().lstrip('__init__() ')}
    except Exception as e:
        return {"error": e.__str__()}
    finally:
        db_session.remove()
        connection.close()


product_and_products_lists = Table(
    'product_and_products_list',
    Base.metadata,
    Column('product_id', ForeignKey('product.id', ondelete="CASCADE"), nullable=False),
    Column('products_list_id', ForeignKey('products_list.id', ondelete="CASCADE"), nullable=False),
    PrimaryKeyConstraint('product_id', 'products_list_id'),
)

currency_and_product = Table(
    'currency_and_product',
    Base.metadata,
    Column('product_id', ForeignKey('product.id', ondelete="CASCADE"), nullable=False,
           ),
    Column('currency_id', ForeignKey('currency.id', ondelete="CASCADE"), nullable=False),
    PrimaryKeyConstraint('product_id', 'currency_id'),
    Column('price', Float),
)


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    product_lists = relationship(
        "ProductsLists",
        backref='user',
        lazy='dynamic',
        cascade="all, delete, delete-orphan"
    )

    def __init__(self, name, login, password, avatar=None):
        self.login = login
        self.password = password
        self.name = name
        if avatar:
            self.avatar = avatar


class Products(Base):
    __tablename__ = 'product'
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    article = Column(String(50))
    title = Column(String(200))
    image = Column(String(100))
    currencies = relationship(
        "Currencies",
        secondary=currency_and_product,
        lazy='dynamic',
    )

    def __init__(self, article, title, image=None):
        self.article = article
        self.title = title
        if image:
            self.image = image


class Currencies(Base):
    __tablename__ = 'currency'
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    title = Column(String(3), unique=True)

    def __init__(self, title):
        self.title = title


class ProductsLists(Base):
    __tablename__ = 'products_list'
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(50))
    products = relationship(
        "Products",
        secondary=product_and_products_lists,
        lazy='dynamic',
    )

    def __init__(self, user_id, title):
        self.user_id = user_id
        self.title = title

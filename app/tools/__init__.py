import string
from random import choice

from app.models.db_api_user import UserDBAPI
from app.models.mysql_tables import Users, session

EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS


def token(n) -> str:
    return ''.join(
        choice(
            f'{string.ascii_uppercase}'
            f'{string.ascii_lowercase}'
            f'{string.digits}'
        ) for _ in range(n)
    )


def check_auth(login, password):
    with session() as s:
        user = s.query(Users).filter(Users.login == login).first()
        if user and user.password == password:
            logged_user = UserDBAPI(id_=user.id)
            return {'sub': logged_user, 'scope': ''}

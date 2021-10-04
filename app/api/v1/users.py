from connexion import NoContent
from flask import request

from app.models.db_api_user import UserDBAPI

users_api = UserDBAPI()


def read_all(sort: str = None, page: int = 1, page_size: int = 5):
    """Read users."""
    users = users_api.get(sort=sort, offset=page-1, page_size=page_size)
    if users and isinstance(users, list):
        return users, 200
    if isinstance(users, dict):
        return users, 500
    return NoContent, 204


def add():
    """Create user."""
    user = users_api.add(user=request.json)
    if user:
        if 'user_id' in user:
            return user, 201
        else:
            return user, 500
    return NoContent, 204


def delete(id_):
    """Delete user by ID."""
    result = users_api.delete(id_=id_)
    if result:
        if 'deleted' in result:
            return result, 200
    return NoContent, 204

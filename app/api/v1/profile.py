import os

from flask import current_app, send_from_directory
from connexion import request, NoContent

from app.models.db_api_user import UserDBAPI
from app.tools import allowed_file


def get(user: UserDBAPI):
    user_data = user.get()
    if user_data:
        return user_data, 200
    return NoContent, 204


def update(user: UserDBAPI):
    new_info = {}
    name = request.form.get('name')
    file = request.files.get('file', None)

    if name:
        new_info.update(name=name)

    if file:
        if all((file.filename != '', allowed_file(file.filename))):
            user_folder = os.path.join(current_app.root_path,
                                       current_app.config['UPLOAD_FOLDER'],
                                       '_'.join(('user', str(user.id_))))
            os.makedirs(user_folder, exist_ok=True)
            file_name = ''.join((
                'avatar.', file.filename.rsplit('.', 1)[1].lower()
            ))
            file.save(os.path.join(user_folder, file_name))
            if os.path.exists(os.path.join(user_folder, file_name)):
                new_info.update(avatar=file_name)
        else:
            return {'error': 'Invalid file'}, 400

    if new_info:
        return user.update(new_info=new_info)
    return NoContent, 204


def avatar(user: UserDBAPI):
    return send_from_directory(
        os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            '_'.join(('user', str(user.id_))),
        ),
        user.avatar(),
        add_etags=False,
        cache_timeout=0,
        last_modified=None,
    )

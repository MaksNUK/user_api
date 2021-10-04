import os
import unicodedata

from connexion import NoContent
from flask import request, current_app, send_from_directory

from app.models.db_api_product import ProductDBAPI
from app.tools import allowed_file

product_api = ProductDBAPI()


def create():
    json_body = request.json
    utf8_json = {key: unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore') for key, value in json_body.items()}
    result = product_api.add(utf8_json)
    if result:
        return result
    return NoContent, 204


def read_all():
    return product_api.read_all()


def delete(id_):
    result = product_api.delete(id_=id_)
    if result:
        return result, 200
    return NoContent, 204


def image(id_):
    new_info = {}
    file = request.files.get('file', None)
    if file:
        if all((file.filename != '', allowed_file(file.filename))):
            products_folder = os.path.join(current_app.root_path,
                                           current_app.config['UPLOAD_FOLDER'],
                                           'products')
            os.makedirs(products_folder, exist_ok=True)
            file_name = ''.join((
                f'product_{id_}.',
                file.filename.rsplit('.', 1)[1].lower()
            ))
            file.save(os.path.join(products_folder, file_name))
            if os.path.exists(os.path.join(products_folder, file_name)):
                new_info.update(image=file_name)
        else:
            return {'error': 'Invalid file'}, 400

    if new_info:
        return product_api.image(id_=id_, new_info=new_info)
    return NoContent, 204


def get_image(id_):
    return send_from_directory(
        os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'products',
        ),
        product_api.get_image(id_),
        add_etags=False,
        cache_timeout=0,
        last_modified=None,
    )

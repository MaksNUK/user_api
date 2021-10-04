import os
import connexion

from app.models.mysql_tables import Base, engine
from app.views import index


def create_app():
    connexion_app = connexion.App(__name__, specification_dir='openapi/')
    connexion_app.add_api(
        os.path.join(os.path.abspath(os.getcwd()), 'swagger.yaml'),
        validate_responses=True,
        base_path='/api/v1.0',
        options={'swagger_url': '/'},
    )
    connexion_app.add_error_handler(404, index.index)

    return connexion_app


application = create_app()
app = application.app
app.config['UPLOAD_FOLDER'] = 'uploads'
Base.metadata.create_all(engine)

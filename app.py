import logging.config

from flask import Flask, Blueprint
from app import settings
from app.control.API import api
from app.control.view.wpsview import ns as viewshed_namespace

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

uri = 'grass'


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint(uri, __name__, url_prefix='/' + uri)
    api.init_app(blueprint)
    api.add_namespace(viewshed_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/' + uri + '/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host='0.0.0.0', debug=settings.FLASK_DEBUG)

if __name__ == '__main__':
    main()

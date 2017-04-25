import os
import logging.config
from app import settings
from app.control.API import api
from flask import Flask, Blueprint, send_from_directory
from app.control.view.wpsview import ns as viewshed_namespace

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')


@app.route('/grass/wps/demo')
def demo():
    return send_from_directory(os.path.join(app.root_path, 'static', 'demo'), 'index.html', mimetype='text/html')


@app.route('/grass/wps/demo/viewshed')
def viewshed():
    return send_from_directory(os.path.join(app.root_path, 'static', 'demo'), 'viewshed.html', mimetype='text/html')


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize(flask_app, flask_app_uri):
    configure_app(flask_app)
    control = Blueprint(flask_app_uri, __name__, url_prefix='/' + flask_app_uri)
    api.init_app(control)
    api.add_namespace(viewshed_namespace)
    flask_app.register_blueprint(control)


if __name__ == '__main__':
    uri = 'grass'
    initialize(app, uri)
    log.info('>>>>> Starting development server at http://{}'.format(app.config['SERVER_NAME'] + '/' + uri + '/ <<<<<'))
    app.run(debug=settings.FLASK_DEBUG)

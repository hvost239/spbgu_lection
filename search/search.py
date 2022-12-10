import os
import json

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    current_app
)

import data_pb2 as Data
from index import Index


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_pyfile(filename='config.cfg')
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.index = Index("../out/")

    @app.route("/", methods=['POST', 'GET'])
    def index():
        return render_template('main.html')


    @app.route("/search")
    def search():
        return app.index.search(request.args['text']);

    return app

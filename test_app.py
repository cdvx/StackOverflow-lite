import pytest

import flask
from models import questionsList

app = flask.Flask(__name__)

with app.test_request_context('/api/v1/questions'):
    assert flask.request.path == '/api/v1/questions'


    def test_getQuestions():

        resp = Response(jsonify({'questions': questionsList}), status=200, mimetype='application/json')



        
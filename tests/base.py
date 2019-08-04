
import os
import tempfile

import pytest, json

from flask import current_app, Response

from application import create_app
from app.utils import DbManager
from app.models import User, Answer, Question

from config import AppConfig, Config
from flask_jwt_extended import (create_access_token, get_jwt_identity)
from datetime import timedelta

conn = DbManager('testing')

@pytest.yield_fixture(scope='session')
def app_():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """
    
    _app = create_app(config_='testing')

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app_):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app_.test_client()


@pytest.fixture(scope='module')
def init_db(app_):
    conn.drop_all()
    conn.create_all()
    yield conn


@pytest.fixture(scope='module')
def request_ctx():
    """
    Setup a request client, this gets executed for each test module.
    :param app: Pytest fixture
    :return: Flask request client
    """
    ctx = current_app.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()


user_data1 = {
        "username": "Kakai",
        "email": "cedriclusiba@gmail.com",
        "password": "jjq123",
        "repeat_password": "jjq123"
    }

@pytest.fixture(scope='function')
def sign_up_user(client):
    conn.drop_all()
    conn.create_all()
    res = client.post(
        '/api/v1/auth/signup', content_type="application/json", data=json.dumps(user_data1))
    assert 'success' in res.json
    return res




@pytest.fixture(scope='function')
def  insert_new_records():
    global queries_
    queries = queries_
    conn.drop_all()
    conn.create_all()
    for query in queries:
        conn.insert_new_record(query[0], query[1])


user1 = User('Peter', 'ptr@gmail.com','1234')
user2 = User('Jane', 'jenn@gmail.com','1234')
question1 = Question('computers', 'what is python ?')
question1.author = user1.username
question2 = Question('api', 'what is Flask ?')
question2.author = user2.username
answer1 = Answer(
    'it is a programming language', question1.id)
answer1.author = user1.username
answer2 = Answer(
    'it a microframework for building python apps', question2.id)
answer2.author = user2.username


queries_ = (('questions', question1.__repr__()), ('questions', question2.__repr__()),
           ('answers', answer1.__repr__()), ('answers', answer2.__repr__()),
           ('users', user1.__repr__()), ('users', user2.__repr__()))


@pytest.fixture(scope='function')
def is_logged_in():
    access_token = create_access_token(
        identity='Peter',
        fresh=timedelta(minutes=200)
    )
    res = Response(mimetype='application/json')
    res.headers['Authorization'] = f'Bearer {access_token}'
    current_user = get_jwt_identity()
    return current_user, res

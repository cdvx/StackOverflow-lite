import os
import tempfile

import pytest, json

from flask import current_app, Response

from application import create_app
from app.connect import conn
from app.models import User, Answer, Question

from config import AppConfig
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from datetime import timedelta



@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """

    _app = create_app(config=AppConfig)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='module')
def init_db(app):
    # conn.create_Answers_table()
#         conn.create_Questions_table()
#         conn.create_Users_table()
    conn.drop_all()
    conn.create_all()
    yield conn
    # conn.session.close()
    conn.drop_all()


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
def sign_up_user(client, init_db):
    conn.drop_all()
    conn.create_all()
    with client:
        res = client.post(
            '/api/v1/auth/signup', content_type="application/json", data=json.dumps(user_data1))
        assert 'success' in res.json
        return res
    conn.drop_all()

__all__ = [
    user_data1, sign_up_user, client, app, request_ctx, init_db
]


@pytest.fixture(scope='function')
def  insert_new_records():
    global queries_
    queries = queries_
    conn.drop_all()
    conn.create_all()
    for query in queries:
        conn.insert_new_record(query[0], query[1])
    # conn.drop_all()


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


ansList = conn.query_all('answers')
qnsList = conn.query_all('questions')
usersList = conn.query_all('users')

@pytest.fixture(scope='function')
def is_logged_in():
    access_token = create_access_token(
        identity='Kakai',
        fresh=timedelta(minutes=200)
    )
    res = Response(mimetype='application/json')
    res.headers['Authorization'] = f'Bearer {access_token}'
    current_user = get_jwt_identity()
    return current_user


# import unittest


# from flask import current_app, Response
# from flask_jwt_extended import (create_access_token, get_jwt_identity,
#                                 jwt_required)
# from flask_testing import TestCase

# from app import app
# from app.connect import DatabaseConnection
# from app.models import Answer, Question, User
# from app.routes import routes
# from config import Config


# class APITestCase(TestCase):

#     def create_app(self):
#         app.config['DEBUG'] = True
#         return app

#     def setUp(self):
#         app = app.test_client()
#         conn = DatabaseConnection()
#         print(conn.dbname)
#         conn.create_Answers_table()
#         conn.create_Questions_table()
#         conn.create_Users_table()
#         data = {
#             "username": "Kakai",
#             "email": "dhhj@gmail.com",
#             "password": "jjq123",
#             "repeat_password": "jjq123"
#         }
#         conn.insert_new_record('users', data)

#         def  insert_new_records(queries):
#             for query in queries:
#                 conn.insert_new_record(query[0], query[1])


#         user1 = User('Peter', 'ptr@gmail.com','1234')
#         user2 = User('Jane', 'jenn@gmail.com','1234')
#         question1 = Question('computers', 'what is python ?')
#         question1.author = user1.username
#         question2 = Question('api', 'what is Flask ?')
#         question2.author = user2.username
#         answer1 = Answer('it is a programming language', 
#                               question1.id)
#         answer1.author = user1.username
#         answer2 = Answer('it a microframework for building python apps', 
#                             #   question2.id)
#         answer2.author = user2.username


#         queries = (('questions', question1.__repr__()), ('questions', question2.__repr__()),
#                         ('answers', answer1.__repr__()), ('answers', answer2.__repr__()),
#                         ('users', user1.__repr__()), ('users', user2.__repr__()))

#         insert_new_records(queries)
        
#         ansList = conn.query_all('answers')
#         qnsList = conn.query_all('questions')
#         usersList = conn.query_all('users')

        
    
#     def is_logged_in(self):
#         access_token = create_access_token(
#             identity='Kakai',
#             fresh=timedelta(minutes=200)
#         )
#         res = Response(mimetype='application/json')
#         res.headers['Authorization'] = f'Bearer {access_token}'
#         current_user = get_jwt_identity()
#         return current_user

#     def tearDown(self):
#         conn.drop_table('users')
#         conn.drop_table('questions')
#         conn.drop_table('answers')


# def createQnsList():
#     '''Generates a List of five questions with different topics
#     and links answers to them'''

#     QnsList = []
#     body = ""

#     topics = [0, '', '', '', '', '']

#     for i in range(1, 6):
#         Qn = Question( topics[i], body)
#         QnsList.append(Qn.__repr__())
#     return QnsList

# questionsList = createQnsList()


# def createAnsList():
#     '''Generates list of five answers'''
#     AnsList = []
#     body = ""

#     l = [question['questionId'] for question in questionsList]
#     qnIds = [id for id in l]
#     qnIds[:0] = [0]

#     for i in range(1, 6):
#         Ans = Answer(body, qnIds[i])
#         AnsList.append(Ans.__repr__())
#     return AnsList

# answersList = createAnsList()

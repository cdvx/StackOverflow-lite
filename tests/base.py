import unittest
from datetime import timedelta

from flask import current_app, Response
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_testing import TestCase

from app import app
from app.connect import DatabaseConnection
from app.models import Answer, Question
from app.routes import routes
from config import Config


class APITestCase(TestCase):

    def create_app(self):
        app.config['DEBUG'] = True
        return app

    def setUp(self):
        self.app = app.test_client()
        self.conn = DatabaseConnection()
        print(self.conn.dbname)
        self.conn.create_Answers_table()
        self.conn.create_Questions_table()
        self.conn.create_Users_table()
        self.data = {
            "username": "Kakai",
            "email": "dhhj@gmail.com",
            "password": "jjq123",
            "repeat_password": "jjq123"
        }
        self.conn.insert_new_record('users', self.data)
    
    def is_logged_in(self):
        self.access_token = create_access_token(
            identity='Kakai',
            fresh=timedelta(minutes=200)
        )
        res = Response(mimetype='application/json')
        res.headers['Authorization'] = f'Bearer {self.access_token}'
        self.current_user = get_jwt_identity()
        return self.current_user

    def tearDown(self):
        self.conn.drop_table('users')
        self.conn.drop_table('questions')
        self.conn.drop_table('answers')


def createQnsList():
    '''Generates a List of five questions with different topics
    and links answers to them'''

    QnsList = []
    body = ""

    topics = [0, '', '', '', '', '']

    for i in range(1, 6):
        Qn = Question( topics[i], body)
        QnsList.append(Qn.__repr__())
    return QnsList

questionsList = createQnsList()


def createAnsList():
    '''Generates list of five answers'''
    AnsList = []
    body = ""

    l = [question['questionId'] for question in questionsList]
    qnIds = [id for id in l]
    qnIds[:0] = [0]

    for i in range(1, 6):
        Ans = Answer(body, qnIds[i])
        AnsList.append(Ans.__repr__())
    return AnsList

answersList = createAnsList()

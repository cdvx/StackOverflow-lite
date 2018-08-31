from flask import json
from flask_testing import TestCase
from tests import app

from app.connect import DatabaseConnection
from app.models import Answer, Question

from .base import APITestCase, answersList, questionsList


class TestModels(APITestCase):

    def setUp(self):

        self.conn = DatabaseConnection()
        
        self.question1 = Question('computers', 'what is python ?')
        self.question2 = Question('api', 'what is Flask ?')
        self.answer1 = Answer('it is a programming language', 
                              self.question1.id)
        self.answer2 = Answer('it a microframework for building python apps', 
                              self.question2.id)
        answersList.append(self.answer1.__repr__())


    def tearDown(self):
        self.conn.drop_table('users')
        self.conn.drop_table('questions')
        self.conn.drop_table('answers')


    def test_answerList_created_properly(self):
        self.assertEqual(6, len(answersList))
        for answer in answersList:
            self.assertIn('answerId', answer)
            self.assertIn('body', answer)
            self.assertIn('Qn_Id', answer)

    def test_answers_questions_have_uniqueIds(self):
        self.assertTrue(self.question1.id != self.question2.id)
        self.assertTrue(self.answer1.answerId != self.answer2.answerId)

    def test_question_answer_relationship(self):
        self.assertTrue(self.question1.id == self.answer1.Qn_Id)
        self.assertTrue(self.answer2.Qn_Id == self.question2.id)


    def test_questionsList_created_properly(self):
        self.assertEqual(5, len(questionsList))
        for question in questionsList:
            self.assertIn('questionId', question)
            self.assertIn('topic', question)
            self.assertIn('body', question)
        

    def test_repr_turnsObject_into_dict(self):
        res1 = self.answer1.__repr__()
        res2 = self.question1.__repr__()
        self.assertTrue(type(res1) == dict)
        self.assertTrue(type(res2) == dict)

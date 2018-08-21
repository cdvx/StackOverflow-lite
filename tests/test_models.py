from flask import json

from app.models import Answer, Question, answersList, questionsList
from tests import app

from .base import APITestCase


class TestModels(APITestCase):

    def setUp(self):
        self.question1 = Question(1, 'computers', 'what is python ?')
        self.answer1 = Answer(1, 'it is a programming language', 1)
        self.question1.answers.append(self.answer1.__repr__())

    def test_answerList_created_properly(self):
        self.assertEqual(5, len(answersList))
        for answer in answersList:
            self.assertIn('answerId', answer)
            self.assertIn('body', answer)
            self.assertIn('Qn_Id', answer)

    def test_questionsList_created_properly(self):
        self.assertEqual(5, len(questionsList))
        for question in questionsList:
            self.assertIn('questionId', question)
            self.assertIn('topic', question)
            self.assertIn('body', question)
    
    def test_questionObject_has_answers_attribute(self):
        self.assertTrue(self.question1.answers)
        self.assertTrue(type(self.question1.answers) == list)
        self.assertTrue(type(self.question1.answers[0]) == dict)        

    def test_repr_turnsObject_into_dict(self):
        res1 = self.answer1.__repr__()
        res2 = self.question1.__repr__()
        self.assertTrue(type(res1))
        self.assertTrue(type(res2))

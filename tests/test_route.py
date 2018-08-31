from datetime import timedelta

from flask import json, url_for
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from tests import app

from .base import APITestCase, questionsList


class TestRoutes(APITestCase):

    def test_root_route(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_user_can_signup(self):
        self.data = {
            "username": "Kakai",
            "email": "cedriclusiba@gmail.com",
            "password": "jjq123",
            "repeat_password": "jjq123"
        }
        res = self.client.post(
            '/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.data))
        msg = {'success': "Kakai's account created successfully"}
        self.assertEqual(res.json, msg)
        self.assertEqual(res.status_code, 200)

    def test_user_can_login(self):
        self.data = {
            "username": "Kakai",
            "email": "cedriclusiba@gmail.com",
            "password": "jjq123",
            "repeat_password": "jjq123"
        }
        res = self.client.post(
            '/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.data))

        self.data2 = {
            "username": "Kakai",
            "password": "jjq123"
        }
        res2 = self.client.post(
            "/api/v1/auth/login", content_type="application/json", data=json.dumps(self.data2))
        
        self.assertEqual(res2.status_code, 200)

    def test_user_can_get_questions(self):
        with self.client:
            questionsList = self.conn.query_all('questions')
            if questionsList:
                res = self.client.get('/api/v1/questions')
                self.assertEqual(res.status_code, 200)

            else:
                res = self.client.get('/api/v1/questions')
                self.assertEqual(res.status_code, 404)
                self.assertEqual(res.json, {'message': 'No Questions added yet'})

    def test_user_can_get_question(self):
        questionsList = self.conn.query_all('questions')
        if questionsList and [qn for qn in questionsList if qn[4]==2]:
            res = self.client.get('/api/v1/questions/2')
            self.assertEqual(res.status_code, 200)
        else:
            res = self.client.get('/api/v1/questions/2')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, {'Question 2': 'does not exist.'})

    def test_user_can_get_answers(self):
        answersList = self.conn.query_all('answers')
        if answersList:
            res = self.client.get('/api/v1/questions/2/answers')
            self.assertEqual(res.status_code, 200)
        else:
            res = self.client.get('/api/v1/questions/2/answers')
            self.assertEqual(res.status_code, 404)

    def test_user_can_get_answer(self):
        answersList = self.conn.query_all('answers')
        if answersList and [ans for ans in questionsList if ans[3]==3 and ans[1]==2]:
            res = self.client.get('/api/v1/questions/2/answers/3')
            for answer in answersList:
                temp = {
                            'answerId': answer[3],
                            'author': answer[4],
                            'body': answer[2],
                            'prefered': answer[5],
                            'QuestionId': answer[1]
                        }
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, temp)
        elif answersList and not [ans for ans in questionsList if ans[1]==2]:
            res = self.client.get('/api/v1/questions/2/answers/3')
            self.assertEqual(res.json, ['Answer not Found'])
            self.assertEqual(res.status_code, 404)
            
        else:
            res = self.client.get('/api/v1/questions/2/answers/3')
            self.assertEqual(res.status_code, 404)
            self.assertEqual(res.json, {'Answer3 for Question2': 'not found.'})

    def test_user_can_post_question(self):
        question = {
                "questionId": 34,
                "topic": "computer science",
                "body": "what is software?"
            }
        if self.is_logged_in() == 'Kakai':
            res = self.client.post('/api/v1/questions', json=question)
            self.assertEqual(res.status_code, 201)
        else:
            res = self.client.post('/api/v1/questions', json=question)
            self.assertEqual(res.status_code, 401)


    def test_user_post_answer(self):
        answer = {
            "answerId": 34,
            "body": "what is software?",
            "Qn_Id": 2
        }
        res = self.client.post('/api/v1/questions/4/answers', json=answer)
        self.assertEqual(res.status_code, 401)

    def test_user_can_update_question(self):

        new_question = {
            "topic": "computer science",
            "body": "what is software?"
        }
        res = self.client.patch('/api/v1/questions/4', json=new_question)
        self.assertEqual(res.status_code, 401)

    def test_user_can_delete_question(self):
        res = self.client.delete('/api/v1/questions/5')
        self.assertEqual(res.status_code, 401)

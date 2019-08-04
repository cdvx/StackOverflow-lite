from datetime import timedelta
import unittest

from flask import json, url_for
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)


from .base import (
    client, app, sign_up_user, sign_up_user,
    user_data1, init_db, conn, insert_new_records,
    ansList, qnsList, usersList, is_logged_in, request_ctx)
from app.connect import DatabaseConnection


def test_root_route(client):
    res = client.get('/')
    assert res.status_code == 200

def test_user_can_signup(client, sign_up_user, init_db):
    msg = {'success': "Kakai's account created successfully"}
    assert sign_up_user.json == msg
    assert sign_up_user.status_code == 201

def test_user_can_login(client, sign_up_user, init_db):
    
    res2 = client.post(
        "/api/v1/auth/login", content_type="application/json", data=json.dumps(user_data1))
    assert 'access_token' in  res2.json
    assert res2.status_code == 200

def test_user_can_get_questions(client, insert_new_records):
    with client:
        questionsList = conn.query_all('questions')
        if questionsList:
            res = client.get('/api/v1/questions')
            assert 'questions' in res.json
            assert res.status_code == 200

        else:
            res = client.get('/api/v1/questions')
            assert res.status_code == 404
            assert res.json == {'message': 'No Questions added.'}
            assert 'message' in res.json

def test_user_can_get_question(client, insert_new_records):
    questionsList = conn.query_all('questions')
    if questionsList and [qn for qn in questionsList if qn[4]==2]:
        res = client.get('/api/v1/questions/2')
        assert 'questionId' in res.json
        assert 'body' in res.json
        assert 'author' in res.json
        assert 'topic' in res.json
        assert res.status_code == 200
    else:
        res = client.get('/api/v1/questions/2')
        assert res.status_code == 200
        assert  res.json == {'message': 'No questions added.'}
        assert 'message' in res.json

def test_user_can_get_answers(client, insert_new_records):
    answersList = conn.query_all('answers')
    if answersList and [ans for ans in qnsList if ans[1]==2 ]:
        res = client.get('/api/v1/questions/2/answers')
        assert res.status_code == 200
        assert 'answers' in res.json
    else:
        res = client.get('/api/v1/questions/2/answers')
        assert res.status_code == 404
        assert 'message' in res.json

def test_user_can_get_answer(client, insert_new_records):
    answersList = conn.query_all('answers')
    if answersList and [ans for ans in qnsList if ans[3]==3 and ans[1]==2]:
        res = client.get('/api/v1/questions/2/answers/3')
        for answer in answersList:
            temp = {
                        'answerId': answer[3],
                        'author': answer[4],
                        'body': answer[2],
                        'prefered': answer[5],
                        'QuestionId': answer[1]
                    }
        assert res.status_code == 200
        assert res.json == temp
        assert 'questionId' in res.json
        assert 'body' in res.json 
        assert 'author' in res.json 
        assert 'topic' in res.json 
        assert 'Qn_Id' in res.json
    elif answersList and not [ans for ans in qnsList if ans[1]==2]:
        res = client.get('/api/v1/questions/2/answers/3')
        assert res.json  ==  ['Answer not found!']
        assert res.status_code == 404
        
    else:
        res = client.get('/api/v1/questions/2/answers/3')
        assert res.status_code == 404
        assert res.json == {'message': 'Question not found!'}
        assert 'message' in res.json

def test_user_can_post_question(client, insert_new_records, is_logged_in, request_ctx):
    question = {
            "questionId": 34,
            "topic": "computer science",
            "body": "what is software?"
        }
    if is_logged_in == 'Kakai':
        res = client.post('/api/v1/questions', json=question)
        assert res.status_code == 201
        assert 'success' in res.json
    else:
        res = client.post('/api/v1/questions', json=question)
        assert res.status_code == 401


def test_user_post_answer(client, insert_new_records, is_logged_in, request_ctx):
    answer = {
        "answerId": 34,
        "body": "what is software?",
        "Qn_Id": 2
    }
    question = {
            "questionId": 34,
            "topic": "computer science",
            "body": "what is software?"
        }
    if is_logged_in == 'Kakai':
        res = client.post('/api/v1/questions', json=question)
        assert res.status_code == 201
        assert 'success' in res.json
    else:
        res = client.post('/api/v1/questions/4/answers', json=answer)
        assert res.status_code == 401

def test_user_can_update_question(client, insert_new_records, is_logged_in, request_ctx):

    new_question = {
        "topic": "computer science",
        "body": "what is software?"
    }
    question = {
            "questionId": 34,
            "topic": "computer science",
            "body": "what is software?"
        }
    if is_logged_in == 'Kakai':
        res = client.post('/api/v1/questions', json=question)
        assert res.status_code == 201
        assert 'success'in res.json
    else:
        res = client.patch('/api/v1/questions/4', json=new_question)
        assert res.status_code == 401

def test_user_can_delete_question(client):
    res = client.delete('/api/v1/questions/5')
    assert res.status_code == 401

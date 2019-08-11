
from flask import json
import unittest
from app.utils import ValidationError


from .base import (
    client, app_, sign_up_user, sign_up_user,
    user_data1, init_db, conn, insert_new_records,
    is_logged_in, request_ctx)


def test_root_route(client):
    res = client.get('/')
    assert res.status_code == 200

def test_user_can_signup(client, sign_up_user, init_db):
    msg = {'success': "Kakai's account created successfully"}
    assert sign_up_user.json == msg
    assert sign_up_user.status_code == 201

def test_user_can_login(client, sign_up_user):
    res2 = None
    res = client.post(
        "/api/v1/auth/login", content_type="application/json", data=json.dumps(user_data1))

    assert 'access_token' in  res.json
    assert res.status_code == 200

def test_signup_fails(client, sign_up_user):
    res = client.post("/api/v1/auth/signup", data={})

    with unittest.TestCase().assertRaises(ValidationError):
        client.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps(user_data1))
    assert res.status_code == 400

def test_pw_dont_match(client):
    
    with unittest.TestCase().assertRaises(ValidationError):
        conn.drop_all()
        conn.create_all()
        c = user_data1.copy()
        c['repeat_password'] = 'rewretgbvfsdgffsgrdhtgsfg'
        client.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps(c))

    r = client.post("/api/v1/auth/signup", content_type="application/json", data=json.dumps({}))
    assert r.status_code == 400
    assert b'message' in r.data
        

def test_login_fails(client, sign_up_user):

    with unittest.TestCase().assertRaises(ValidationError):
        res = client.post("/api/v1/auth/login")

    with unittest.TestCase().assertRaises(ValidationError):
        x = user_data1.copy()
        del x['username']
        del x['email']
        client.post("/api/v1/auth/login", content_type="application/json", data=json.dumps(x))
    with unittest.TestCase().assertRaises(ValidationError):
        r = user_data1.copy()
        del r['email']
        del r['password']
        client.post("/api/v1/auth/login", content_type="application/json", data=json.dumps(r))

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
    if questionsList :
        res = client.get(f'/api/v1/questions/{questionsList[0][4]}')
        assert 'questionId' in res.json
        assert 'body' in res.json
        assert 'author' in res.json
        assert 'topic' in res.json
        assert res.status_code == 200


def test_user_can_get_answers(client, insert_new_records):
    answersList = conn.query_all('answers')
    qnsList = conn.query_all('questions')
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
    qtns = conn.query_all('questions')
    if answersList:
        id_ = [qn[4] for qn in qtns if qn[3] == 'Peter']
        ids = lambda ids: ids.pop()

        _id = [ans[3] for ans in conn.query_all('answers') if ans[1] == id_[0]]

        res = client.get(f'/api/v1/questions/{id_[0]}/answers/{_id[0]}')

        assert res.status_code == 200
        assert 'QuestionId' in res.json
        assert 'body' in res.json 
        assert 'author' in res.json 
    elif answersList and not [ans for ans in qtns if ans[1]==2]:
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

    _, logged_in_res = is_logged_in
    
    res = client.post('/api/v1/questions', json=question, headers=logged_in_res.headers)
    assert res.status_code == 201
    assert 'success' in res.json


def test_user_post_prefer_answer(client, insert_new_records, is_logged_in, request_ctx):
    answer = {
        "answerId": 2,
        "body": "what is software?",
        "Qn_Id": 2
    }

    _, logged_in_res = is_logged_in
    id_ = [qn[4] for qn in conn.query_all('questions') if qn[3] == 'Peter']
    
    answer['Qn_Id'] = id_[0]
    res = client.post(f'/api/v1/questions/{id_[0]}/answers', json=answer, headers=logged_in_res.headers)

    res_ = client.put(f"/api/v1/questions/{id_[0]}/answers/{res.json['answer']['answerId']}", headers=logged_in_res.headers)
    assert res.status_code == 201
    assert res_.status_code == 201

def test_user_can_update_question(client, insert_new_records, is_logged_in, request_ctx):
    new_question = {
        "topic": "computer science",
        "body": "what is software?"
    }

    is_logged_in1, logged_in_res = is_logged_in
    qtns = conn.query_all('questions')
        
    id_ = [qn[4] for qn in qtns if qn[3] == 'Peter']
    res = client.patch(
        f'/api/v1/questions/{id_[0]}', json=new_question,
        headers=logged_in_res.headers
        )
    assert res.status_code == 200

def test_user_can_delete_question(client, is_logged_in):
    _, logged_in_res = is_logged_in
    id_ = [qn[4] for qn in conn.query_all('questions') if qn[3] == 'Peter']
    res = client.delete(f'/api/v1/questions/{id_[0]}', headers=logged_in_res.headers)

    assert res.status_code == 200

# def test_user_can_delete_answer(client, is_logged_in):
#     _, logged_in_res = is_logged_in
#     id_ = [qn[4] for qn in conn.query_all('questions') if qn[3] == 'Jane']
#     _id = [ans[1] for ans in conn.query_all('answers') if ans[4] == 'Jane']
#     print('\n\n >>>>>>>>', _id)
#     res = client.delete(f'/api/v1/questions/{id_[0]}/answers/{_id[0]}', headers=logged_in_res.headers)
#     assert res.status_code == 200

import uuid

from werkzeug.security import generate_password_hash

from app.connect import conn
from app.utils import ValidationError


class Question:
    def __init__(self, topic, body, author=None):
        self.id = uuid.uuid4().int
        self.topic = str(topic).strip()
        self.body = str(body).strip()
        self.author = author

    def __repr__(self):
        return {
            'topic': self.topic,
            'body': self.body,
            'questionId': self.id,
            'author': self.author
        }


class Answer:
    def __init__(self, body, Qn_Id, author=None, pref=False):
        self.answerId = uuid.uuid4().int
        self.body = str(body).strip()
        self.Qn_Id = Qn_Id
        self.author = author
        self.prefered = pref

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body,
            'author': self.author,
            'prefered': self.prefered
        }


class User:
    def __init__(self, username, email, password):
        self.id = uuid.uuid4().int
        self.username = str(username).strip()
        self.email = str(email).strip()
        self.password_hash = generate_password_hash(str(password))
    
    def __repr__(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password_hash,
            'user_id': self.id
        }


def valid_username(username):
    user = conn.get_user(username)
    if user:
        return False
    return True

def valid_email(email):
    user = conn.get_user(email)
    if user:
        return False
    return True


def valid_question(questionObject):
    if 'topic' in questionObject.keys() and 'body' in questionObject.keys():

        questionsList = conn.query_all('questions')
        input_topic = questionObject['topic']
        input_body = questionObject['body']

        empty_field = len(str(input_topic).strip()) == 0 or len(str(input_body).strip()) == 0
        check_type = type(input_topic) == int or type(input_body) == int
        if empty_field or check_type:
            value = (False, {"hint_1":"Question topic or body should not be empty!",
                            "hint_2":"body and topic fileds should not consist entirely of integer-type data"})
            return value
        if questionsList:
            topics = [question[1] for question in questionsList if question[1] == input_topic]
            if len(topics) != 0:
                value = (False, "Question topic already exists!")
                return value             
            else:
                if len(topics) == 0:
                    return (True, )
        return (True, )
    else:
        if 'topic' or 'body' not in questionObject.keys():
            return (False, )
 

def valid_answer(answerObject):
    if 'body' in answerObject.keys():
        input_body = answerObject['body']
        empty_field = len(input_body.strip()) == 0
        check_type = type(input_body) == int
        if empty_field or check_type:
            return (False, {'message': "Answer body should not be empty!"+
                             """body and Qn_Id fileds should not contain
                            numbers only and string-type data respectively"""}
                )
        return (True, )
    else:
        return (False, )


def valid_signup_data(request_data):
    keys = request_data.keys()
    email, username, password, repeat_password = (
        request_data.get('email'),
        request_data.get('username'),
        request_data.get('password'),
        request_data.get('repeat_password')
    )
    condition_1 = 'username' and 'email' and 'repeat_password' and 'password' in keys
    condition_2 =  email and username and password and repeat_password
    
    if condition_1 and condition_2:
        return True
    return False



def valid_login_data(request_data):
    keys = request_data.keys()
    email, username, password = (
        request_data.get('email'),
        request_data.get('username'),
        request_data.get('password')
    )
    condition_1 = 'username' or 'email' in keys and 'password' in keys
    condition_2 =  email or username and password
    
    if condition_1 and condition_2:
        return True
    return False


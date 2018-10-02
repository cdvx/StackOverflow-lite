from datetime import datetime, timedelta

from flask import (Flask, Response, make_response,
                   json, jsonify, request, url_for)
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash

from app import (app, internal_server_error, url_unknown,
                 method_not_allowed, forbidden_resource, deleted_resource)
from app.connect import conn
from app.models import (Answer, Question, User, valid_answer, valid_login_data,
                        valid_question, valid_signup_data, valid_username)

origin = 'httsp://stackoverflowlite-cdvx-fronted.herokuapp.com'

@app.route('/')
def show_api_works():
    return jsonify({'Welcome to my app': [{'message': "endpoints work"}]})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():

    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'JSON missing in request!'}), 400

    if valid_login_data(request_data):
        username = request_data['username']
        password = request_data['password']

        if not username:
            return jsonify({
                'message': 'Required parameter: username missing!'
            }), 400
        elif not password:
            return jsonify({
                'message': 'Required parameter: password missing!'
            }), 400

        users = conn.query_all('users')
        user = [user for user in users if check_password_hash(
            user[3], str(password)) and user[1] == username]
        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401

        access_token = create_access_token(
            identity=username,
            fresh=timedelta(minutes=1440)
        )
        # headers = {''}
        msg = {'access_token': f'{access_token}'}
        response = make_response(jsonify(msg))
        response.headers.add('Acess-Control-Allow-Origin', origin)
        response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
        return response, 200
    msg = {"message": "Invalid login data",
           "Hint": """required formart is: {'username':'xyz',
                    'password': 'xyh12',}"""}
    return jsonify(msg), 400


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'JSON missing in request!'}), 400

    if valid_signup_data(request_data):
        username = str(request_data['username']).strip().split()
        email = request_data['email']
        password = request_data['password']
        repeat_password = request_data['repeat_password']

        if not username:
            return jsonify({
                'message': 'Required parameter: username missing!'
            }), 400
        elif username:
            if len(username) > 1:
                username_ = username[0] + " " + username[1]
                username = username_
                if not valid_username(username):
                    return jsonify({'message': f'Username: {username} already taken!'}), 401
            else:
                if len(username) == 1:
                    username = username[0]
                    if not valid_username(username):
                        return jsonify({'message': f'Username: {username} already taken!'}), 401

        if not email or len(email.strip()) == 0:
            return jsonify({'message': 'Required parameter: email missing!'}), 400
        if username and email:
            if not password or len(str(password).strip()) == 0:
                return jsonify({'message': 'Required parameter: password missing!'}), 400

        if username and email and password:
            if not repeat_password or len(str(repeat_password).strip()) == 0:
                msg = 'Required parameter: repeat_password missing!'
                return jsonify({'message': f'{msg}'}), 400
            else:
                if repeat_password:
                    if  repeat_password == password:
                        user = User(username, email, password)
                        conn.insert_new_record('users', user.__repr__())

                        response = make_response(jsonify({
                            'success': f"{username}'s account created successfully"}))
                        response.headers.add('Acess-Control-Allow-Origin', origin)
                        response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
                        return response, 201
                    if repeat_password and repeat_password != password:
                        return jsonify({
                            'message': 'Password does not match repeat_password'
                        }), 401
    msg = {"error": "Invalid signup data",
        "Hint": """required formart is: {'username':'xyz',
                    'email':'xyz@gmail.com',
                    'password': 'xyh12',
                    'repeat_password':'xyh12'}"""}
    return jsonify(msg), 400


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    questionsList = conn.query_all('questions')
    questions = []
    print(questionsList)
    if questionsList:
        for qn in questionsList:
            temp = {
                'questionId': qn[4],
                'author': qn[3],
                'topic': qn[1],
                'body': qn[2]
            }
            questions.append(temp)
        return jsonify({'questions': questions}), 200
    response = make_response(jsonify({'message': 'No Questions added.'}))
    return response, 404


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    ans_list= []
    
    if questionsList:
        question = [qn for qn in questionsList if int(qn[4])==questionId]
        if question and not answersList:
            temp = {
                'questionId': question[0][4],
                'topic': question[0][1],
                'body': question[0][2],
                'author': question[0][3]
            }
            return jsonify(temp), 200
        if question and answersList:
            answers = [ans for ans in answersList if int(ans[1]) == questionId]
            if answers:
                for ans in answers:
                    temp1 = {
                        'answerId': ans[3],
                        'body': ans[2],
                        'author': ans[4],
                        'prefered': ans[5],
                        'questionId': ans[1]
                    }
                    
                    ans_list.append(temp1)
                temp = {
                    'questionId': question[0][4],
                    'topic': question[0][1],
                    'body': question[0][2],
                    'author': question[0][3],
                    'answers': ans_list
                }
                return jsonify(temp), 200
            
        return jsonify({'message': 'No answers added'}), 404
        
    return jsonify({'message': 'No questions added.'}), 200


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    answersList = conn.query_all('answers')
    questionsList = conn.query_all('questions')
    if questionsList:
        questions = [qn for qn in questionsList if int(qn[4]) == questionId]
        print(questions)
        if questions:
            answers = []
            if answersList:
                for answer in answersList:
                    if int(answer[1]) == questionId:
                        temp = {
                            'answerId': answer[3],
                            'author': answer[4],
                            'body': answer[2],
                            'prefered': answer[5],
                            'questionId': answer[1]
                        }
                        answers.append(temp)
                        return jsonify({'answers': answers}), 200
                    return jsonify({'message': 'Answer not found!'}), 404
            return jsonify({'message': 'No Answers added.'}), 404
        return jsonify({'message': 'Question not found!'}), 404
    return jsonify({'message': 'No questions added!'}), 404


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>',
           methods=['GET'])
def get_answer(questionId, answerId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    if questionsList:
        if answersList:
            for answer in answersList:
                
                if int(answer[3]) == answerId:
                
                    temp = {
                        'answerId': answer[3],
                        'author': answer[4],
                        'body': answer[2],
                        'prefered': answer[5],
                        'QuestionId': answer[1]
                    }
                    return jsonify(temp), 200
        return Response(json.dumps(['Answer not found!']),
                        status=404, mimetype='application/json')
    return jsonify({'message': 'Question not found!'}), 404


@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def add_question():

    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()

        duplicate_check = valid_question(request_data)

        if duplicate_check[0]:
            temp = {
                'topic': request_data['topic'],
                'body': request_data['body']
            }

            question = Question(temp['topic'], temp['body'])
            question.author = current_user
            conn.insert_new_record('questions', question.__repr__())

            response = make_response(jsonify({
                'success': 'Question posted successfully',
                'question': question.__repr__()
            }))
            response.headers.add('Acess-Control-Allow-Origin', origin)
            response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
            return response, 201

        else:
            if not duplicate_check[0] and len(duplicate_check) > 1:
                reason = duplicate_check[1]
                return jsonify({"message": f"{reason}"})
            else:
                bad_object = {
                    "message": "Invalid question object",
                    "hint": '''Request format should be,{'topic': 'python',
                        'body': 'what is python in programming' }'''
                }
                response = Response(json.dumps([bad_object]),
                                    status=400, mimetype='application/json')
                return response
    return jsonify({
        'message': 'To post a question, you need to be logged in',
        'info': 'Signup or login, to get acces_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList:
            answer_check = valid_answer(request_data)
            ids = [int(qn[4]) for qn in questionsList]
            if answer_check[0] and questionId in ids:
                temp = {
                    'Qn_Id': questionId,
                    'body': request_data['body']
                }
                answer = Answer(temp['body'], temp['Qn_Id'])
                answer.author = current_user
                conn.insert_new_record('answers', answer.__repr__())

                response = make_response(jsonify({
                    'success': 'Answer posted successfully',
                    'answer': answer.__repr__()
                }))
                response.headers.add('Acess-Control-Allow-Origin', origin)
                response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
                return response, 201

            else:

                if not answer_check[0] and len(answer_check) > 1:
                    reason = answer_check[1]
                    return jsonify({"message": f"{reason}"})
                else:
                    bad_object = {
                        "error": "Invalid answer object",
                        "hint": '''Request format should be {
                            'body': 'this is the body',
                                'Qn_Id': 2}'''
                    }

                    return jsonify({'message': bad_object}), 400
        msg = {f'Attempt to answer Question with Id:{questionId}':
               'Question not found!.'}
        return jsonify({'message': msg}), 404

    return jsonify({
        'message': 'To post an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def select_answer_as_preferred(questionId, answerId):
    current_user = get_jwt_identity()
    if current_user:
        # request_data = request.get_json()
        questionsList = conn.query_all('questions')
        answersList = conn.query_all('answers')

        if answersList or questionsList:

            #answer_check = valid_answer(request_data)
            usr = [qn[3] for qn in questionsList if int(qn[4]) == questionId]

            answer = [ans for ans in answersList if int(ans[1]) == questionId and int(ans[3]) == answerId]
            
            if usr and usr[0] == current_user:

                if answer[0]:

                    conn.update_answer(str(answerId))
                    temp = {
                        'answerId': answer[0][3],
                        'body': answer[0][2],
                        'author': answer[0][4],
                        'prefered': True,
                        'questionId': answer[0][1]
                    }

                    response = make_response(jsonify({
                        'success': "Answer marked as preferred",
                        'answer': temp
                    }))
                    response.headers.add('Acess-Control-Allow-Origin', origin)
                    response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
                    return response, 201
    
                return jsonify({'message': 'Answer not found!'}), 404
            return jsonify({'message':
                            f'Only question auhtor:{current_user} can perform this action!'})
        return jsonify({'message':
                        'Question not found'}), 404

    return jsonify({
        'message': 'To prefer an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
@jwt_required
def update_question(questionId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList:
            usr = [qn[3] for qn in questionsList if int(qn[4]) == questionId]
            if usr and usr[0] == current_user:
                ids = [int(question[4]) for question in questionsList]

                if questionId in ids:
                    result = valid_question(request_data)
                    if result[0]:
                        for question in questionsList:
                            if int(question[4]) == questionId:
                                conn.update_question(
                                    request_data['topic'],
                                    request_data['body'],
                                    str(questionId))
                                temp = {
                                    'new_topic': request_data['topic'],
                                    'new_body': request_data['body']
                                }
                                msg = 'Question updated successfully.'

                                response = make_response(jsonify({'success': msg,
                                                         'updated_question': temp}))
                                response.headers.add('Acess-Control-Allow-Origin', origin)
                                response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
                                return response, 200
                    if not result[0] and len(result) > 1:
                        msg = {'message':result[1]}
                        return jsonify(msg), 400
                    if not result[0] and len(result) ==1:
                        bad_object = {
                            "error": "Invalid answer object",
                            "hint": '''Request format should be {
                                'body': 'this is the body',
                                    'Qn_Id': 2}'''
                        }
                        return jsonify({'message': bad_object}), 400

                return jsonify({'message':'Question not found'}), 404

            msg = f'Only question auhtor:{current_user} can perform this action!'
            return jsonify({'message': msg}), 401
        
        return jsonify({'message': 'No questions added'}), 404
    return jsonify({
        'message': 'To update a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    current_user = get_jwt_identity()
    if current_user:
        questionsList = conn.query_all('questions')
        if questionsList:
            usr = [qn[3] for qn in questionsList if int(qn[4]) == questionId]
            if usr and usr[0] == current_user:
                ids = [int(question[4]) for question in questionsList]
                if questionId in ids:

                    for question in questionsList:
                        if questionId == int(question[4]):

                            questionsList.remove(question)
                            conn.delete_entry('questions', str(questionId))

                            message = {
                                'success': f"Question deleted!"}

                            response = make_response(jsonify({'success': message}))
                            response.headers.add('Acess-Control-Allow-Origin', origin)
                            response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
                            return response, 200
            msg = f'Only question auhtor:{current_user} can perform this action!'
            return jsonify({'message': msg}), 401
        return jsonify({'message': 'Question not found'}), 404
    return jsonify({
        'message': {'To delete a question, you need to be logged in':
                    'Signup or login, to get access_token'}}), 401





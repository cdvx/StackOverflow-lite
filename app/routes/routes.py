from datetime import datetime, timedelta

from flask import Flask, Response, json, jsonify, request, url_for
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from werkzeug.security import check_password_hash
from app import app
from app.models import (Answer, Question, User, valid_answer, valid_login_data,
                        valid_question, valid_username, valid_signup_data)
from app.connect import conn


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
            fresh=timedelta(minutes=60)
        )
        msg = {'access_token': f'{access_token}'}

        return jsonify({f'access token created for user {username}': msg}), 200
    msg = {"error": "Invalid login data",
           "Hint": """required formart is: {'username':'xyz',
                    'password': 'xyh12',}"""}
    return jsonify(msg)


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'JSON missing in request!'}), 400

    if valid_signup_data(request_data):
        username = str(request_data['username']).split()
        email = request_data['email']
        password = request_data['password']
        repeat_password = request_data['repeat_password']

        if not username:
            return jsonify({
                'message': 'Required parameter: username missing!'
            }), 400
        else:
            if username:
                if len(username) > 1:
                    username_ = username[0] + " " + username[1]
                    username = username_
                    if not valid_username(username):
                        return jsonify({'message': f'username {username} already taken!'}), 401
                elif len(username) == 1:
                    username = username[0]
                    if not valid_username(username):
                        return jsonify({'message': f'username {username} already taken!'}), 401
                if not email:
                    return jsonify({'message': 'Required parameter: email missing!'}), 400
                elif not password:
                    return jsonify({'message': 'Required parameter: password missing!'}), 400
                else:
                    if not repeat_password:
                        msg = 'Required parameter: repeat_password missing!'
                        return jsonify({'message': f'{msg}'}), 400

                if repeat_password == password:

                    user = User(username, email, password)
                    conn.insert_new_record('users', user.__repr__())
                
                    return jsonify({
                        'success': f"{username}'s account created successfully"
                    }), 200
                else:
                    if repeat_password != password:
                        return jsonify({
                            'message': 'Password does not match repeat_password'
                        }), 401
    msg = {"error": "Invalid signup data",
           "Hint": """required formart is: {'username':'xyz',
                    'email':'xyz@gmail.com',
                    'password': 'xyh12',
                    'repeat_password':'xyh12'}"""}
    return jsonify(msg)


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    questionsList = conn.query_all('questions')
    questions = []
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
    return jsonify({'message': 'No Questions added yet'}), 404


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    answers = [[ans[2]] for ans in answersList if int(ans[1]) == questionId]
    if questionsList:
        for question in questionsList:
            if int(question[4]) == questionId:
                temp = {
                    'questionId': question[4],
                    'topic': question[1],
                    'body': question[2],
                    'author': question[3],
                    'answers': answers
                }
                return jsonify(temp), 200
        return Response(json.dumps(['Question not Found']),
                        status=404, mimetype='application/json')
    return jsonify({f'Question {questionId}': 'does not exist.'}), 200


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    answersList = conn.query_all('answers')
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
    return jsonify({'message': f'No Answers added for question {questionId}.'}), 404


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
            return Response(json.dumps(['Answer not Found']),
                            status=404, mimetype='application/json')
    return jsonify({
        f'Answer{answerId} for Question{questionId}': 'not found.'
    }), 404


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

            return jsonify({
                'msg': f'Question {question.id} posted successfully',
                'Posted by': f'{current_user}'
            }), 201

        else:
            if not duplicate_check[0] and len(duplicate_check) > 1:
                reason = duplicate_check[1]
                return jsonify({"error": f"{reason}"})
            else:
                bad_object = {
                    "error": "Invalid question object",
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
            if answer_check[0]:
                temp = {
                    'Qn_Id': questionId,
                    'body': request_data['body']
                }
                answer = Answer(temp['body'], temp['Qn_Id'])
                answer.author = current_user
                conn.insert_new_record('answers', answer.__repr__())

                return jsonify({
                    'msg': f'Answer {answer.answerId} posted successfully'
                }), 201

            else:

                if not answer_check[0] and len(answer_check) > 1:
                    reason = answer_check[1]
                    return jsonify({"error": f"{reason}"})
                else:
                    bad_object = {
                        "error": "Invalid answer object",
                        "hint": '''Request format should be {
                            'body': 'this is the body',
                                'Qn_Id': 2}'''
                    }
                    response = Response(json.dumps([bad_object]),
                                        status=400, mimetype='application/json')
                    return response
        return jsonify({f'Attempt to answer Question {questionId}':
                        f'Question {questionId} does not exist.'}), 404

    return jsonify({
        'message': 'To post an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def select_answer_as_preferred(questionId, answerId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')

        if questionsList:

            #answer_check = valid_answer(request_data)
            usr = [qn[3] for qn in questionsList if int(qn[4]) == questionId]
            
            if usr and usr[0] == current_user:

                conn.update_answer(str(answerId))

                return jsonify({
                    'msg': f"Answer {answerId} marked as preferred"
                }), 201
            else:

                if not answer_check[0] and len(answer_check) > 1:
                    reason = answer_check[1]
                    return jsonify({"error": f"{reason}"})
                else:
                    bad_object = {
                        "error": "Invalid answer object",
                        "hint": '''Request format should be {
                            'body': 'this is the body',
                                'Qn_Id': 2}'''
                    }
                    response = Response(json.dumps([bad_object]),
                                        status=400, mimetype='application/json')
                    return response
            return jsonify({'Access denied':
                            f'Only question auhtor:{current_user} can perform this action!'})
        return jsonify({f'Attempt to select answer to Question {questionId} as prefered':
                        f'Question {questionId} does not exist.'}), 404

    return jsonify({
        'message': 'To post an answer, you need to be logged in',
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
                updated_question = dict()
                ids = [int(question[4]) for question in questionsList]

                if questionId in ids:
                    if "topic" in request_data:
                        updated_question["topic"] = request_data["topic"]
                    if "body" in request_data:
                        updated_question["body"] = request_data["body"]
                    condition_1 = len(updated_question['topic'])
                    condition_2 = len(updated_question['body'])
                    if condition_1 != 0 and condition_2 != 0:
                        for question in questionsList:
                            if int(question[4]) == questionId:
                                conn.update_question(
                                    updated_question['topic'],
                                    updated_question['body'],
                                    str(questionId))
                                msg = f'Question {questionId} updated successfully.'
                                return jsonify({'msg': msg}), 200
                    return jsonify({
                        'msg': 'body and topic fields should not be empty'})
            msg = f'Only question auhtor:{current_user} can perform this action!'
            return jsonify({'Access denied': msg})
        response = Response(json.dumps(['Question not found']), status=404)
        return response

    return jsonify({
        'message': 'To update a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    })


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
                                'success': f"Question {questionId} deleted successfully!"}
                            response = Response(
                                json.dumps(message), status=202, mimetype='application/json')
                            return response
            msg = f'Only question auhtor:{current_user} can perform this action!'
            return jsonify({'Access denied': msg})
        response = Response(json.dumps(['Question not found']),
                            status=404, mimetype='application/json')
        return response
    return jsonify({
        'message': 'To delete a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.errorhandler(500)
def internal_sserver_error(e):
    msg = "Sorry,we are experiencing some technical difficulties"
    msg2 = "Please report this to cedriclusiba@gmail.com and check back with us soon"
    return jsonify({'error': msg, "hint": msg2}), 500


@app.errorhandler(404)
def url_unknown(e):
    msg = "Sorry, resource you are looking for does not exist"
    return jsonify({"error": msg}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    msg = "Sorry, this action is not supported for this url"
    return jsonify({'error': msg}), 405


@app.errorhandler(403)
def forbidden_resource(e):
    msg = "Sorry, resource you are trying to access is forbidden"
    return jsonify({'error': msg}), 403


@app.errorhandler(410)
def deleted_resource(e):
    return jsonify({'error': "Sorry, this resource was deleted"}), 410

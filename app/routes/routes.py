from flask import (Flask, Response, flash, json, jsonify,
                     request, session, url_for)

from app import app
from app.models import Answer, Question, answersList, questionsList


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions': questionsList})

@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    for question in questionsList:
        if question['questionId'] == questionId:
            temp = {
                'questionId': question['questionId'],
                'topic': question['topic'],
                'body': question['body']
            }
            return jsonify(temp)
    return Response(json.dumps(['Question not Found']), 
                    status=404, mimetype='application/json')


@app.route('/api/v1/questions', methods=['POST'])
def add_question():

    request_data = request.get_json()
    if (valid_question(request_data)):
        temp = {
            'questionId': request_data['questionId'],
            'topic': request_data['topic'],
            'body': request_data['body']
        }
        questionsList.append(temp)
        response = Response('', 201, mimetype='application/json')
        response.headers['location'] = ('questions/' + 
                                        str(request_data['questionId']))
        
        return response
    else:
        bad_object = {
            "error": "Invalid question object",
            "hint": '''Request format should be,{'questionId':1, 'topic': 'python',
                'body': 'what is python in programming' }'''
        }
        response = Response(json.dumps([bad_object]), 
                            status=400, mimetype='application/json')
        return response

@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def add_answer(questionId):
    request_data = request.get_json()
    if (valid_answer(request_data)):
        temp = {
            'answerId': request_data['answerId'],
            'Qn_Id': request_data['Qn_Id'],
            'body': request_data['body']
        }
        answersList.append(temp)
        for question in questionsList:
            if question['questionId'] == request_data['Qn_Id']:
                question = Question(question['questionId'], 
                                    question['topic'], question['body'])
                question.answers.append(temp)

        response = Response('', status=201, mimetype='application/json')
        response.headers['location'] = ('answers/' + 
                                        str(request_data['answerId']))
        return response
    
    else:
            bad_object = {
                "error": "Invalid answer object",
                "hint": '''Request format should be {'answerId':1, 
                'body': 'this is the body',
                    'Qn_Id': 2}'''
            }
            response = Response(json.dumps([bad_object]), 
                                status=400, mimetype='application/json')
            return response




def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        return True
    else:
        return False

def valid_answer(answerObject):
    if 'Qn_Id' in answerObject and 'answerId' in answerObject and 'body' in answerObject :
        return True
    else:
        return False
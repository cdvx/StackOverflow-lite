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





def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        return True
    else:
        return False
        
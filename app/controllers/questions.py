
from app.controllers.imports import *


questions = Blueprint("questions", __name__)


@questions.route('/api/v1/questions', methods=['GET'])
def get_questions():
    questionsList = conn.query_all('questions')
    questions = []
    if questionsList:
        for qn in questionsList:
            temp = { #pragma: no cover
                'questionId': qn[4],
                'author': qn[3],
                'topic': qn[1],
                'body': qn[2]
            }
            questions.append(temp)
        return jsonify({'questions': questions}), 200 #pragma: no cover
    response = make_response(jsonify({'message': 'No Questions added.'})) #pragma: no cover
    return response, 404 #pragma: no cover


@questions.route('/api/v1/questions/<int:questionId>', methods=['GET'])
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
        elif question and answersList:
            answers = [ans for ans in answersList if int(ans[1]) == questionId]  #pragma: no cover
            if answers: #pragma: no cover
                for ans in answers:
                    temp1 = {
                        'answerId': ans[3],
                        'body': ans[2],
                        'author': ans[4],
                        'prefered': ans[5],
                        'questionId': ans[1]
                    }
                    
                    ans_list.append(temp1)  #pragma: no cover
                temp = {
                    'questionId': question[0][4],
                    'topic': question[0][1],
                    'body': question[0][2],
                    'author': question[0][3],
                    'answers': ans_list
                }
                return jsonify(temp), 200  #pragma: no cover
            
            else: 
                return jsonify({'message': 'No answers added'}), 404  #pragma: no cover
        
    return jsonify({'message': 'No questions added.'}), 200  #pragma: no cover



@questions.route('/api/v1/questions', methods=['POST'])
@jwt_required
def add_question():

    current_user = get_jwt_identity()
    request_data = request.get_json()
    duplicate_check = valid_question(request_data)
    if current_user and duplicate_check[0]:
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
        if current_user and len(duplicate_check) > 1:  #pragma: no cover
            reason = duplicate_check[1]
            return jsonify({"message": f"{reason}"})
        else:
            bad_object = {  #pragma: no cover
                "message": "Invalid question object",
                "hint": '''Request format should be,{'topic': 'python',
                    'body': 'what is python in programming' }'''
            } if current_user else {
                'message': 'To post a question, you need to be logged in',
                    'info': 'Signup or login, to get acces_token'
                }
            response = Response(json.dumps([bad_object]),  #pragma: no cover
                                status=400 if current_user else 401, mimetype='application/json')
            return response  #pragma: no cover



@questions.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
@jwt_required
def update_question(questionId):
    current_user = get_jwt_identity()
    request_data = request.get_json()
    question = conn.get_question(str(questionId))

    if current_user and question:
        author = question[3] == current_user
        result = valid_question(request_data)

        if author and result[0]:
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
        elif not author or len(result) > 1:  #pragma: no cover
            msg = {'message':result[1]} if not author else {
                    'message': f'Only author: {question[3]} can update this question!'
                } #pragma: no cover
            return (jsonify(msg), 401 if author else 400)

        else:
            handle_not_author(author, result, question) #pragma: no cover
    elif not current_user:#pragma: no cover
        return jsonify({    #pragma: no cover
                        'message': 'To update a question, you need to be logged in',
                        'info': 'Signup or login, to get access_token'
                    }), 401
    else:
        if not question: #pragma: no cover
            return jsonify({'message':'Question not found'}), 404

def handle_not_author(author, result, question):
    if not author or len(result) == 1: #pragma: no cover
        bad_object = { #pragma: no cover
            "error": "Invalid answer object",
            "hint": '''Request format should be {
                'body': 'this is the body',
                    'Qn_Id': 2}'''
        } if not author else { 
                'message': 
                f'Only author: {question[3]} can update this question!'
            }
        return (jsonify({'message': bad_object}), 401 if author else 400)  #pragma: no cover


@questions.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    current_user = get_jwt_identity()
    question = conn.get_question(str(questionId))

    if current_user and question:
        author = question[3] == current_user
        if author:
            conn.delete_entry('questions', str(questionId))

            message = {
                'success': f"Question deleted!"}

            response = make_response(jsonify({'success': message}))
            response.headers.add('Acess-Control-Allow-Origin', origin)
            response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
            return response, 200
        msg = f'Only question auhtor:{current_user} can perform this action!'
        return jsonify({'message': msg}), 401 #pragma: no cover

    return (jsonify({'message': 'Question not found'}), 404)  if not question \
        else  jsonify({  #pragma: no cover
        'message': {'To delete a question, you need to be logged in': #pragma: no cover
                'Signup or login, to get access_token'}}), 401 #pragma: no cover \

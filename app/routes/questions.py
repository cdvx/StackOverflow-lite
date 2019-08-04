

from app.routes.imports import *


questions = Blueprint("questions", __name__)


@questions.route('/api/v1/questions', methods=['GET'])
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
    response = make_response(jsonify({'message': 'No Questions added.'}))
    return response, 404


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
            
            else: 
                return jsonify({'message': 'No answers added'}), 404
        
    return jsonify({'message': 'No questions added.'}), 200



@questions.route('/api/v1/questions', methods=['POST'])
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


@questions.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
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


@questions.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
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





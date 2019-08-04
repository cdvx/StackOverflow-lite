
from app.routes.imports import *


answers = Blueprint("answers", __name__)

@answers.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    answersList = conn.query_all('answers')
    questionsList = conn.query_all('questions')
    if questionsList and [qn for qn in questionsList if int(qn[4]) == questionId]:
 
        if answersList:
            answers = [
                {
                    'answerId': answer[3],
                    'author': answer[4],
                    'body': answer[2],
                    'prefered': answer[5],
                    'questionId': answer[1]
                } for answer in answersList if int(answer[1]) == questionId]
            return (jsonify({'answers': answers}), 200) if answers else (jsonify({'message': 'Answer not found!'}), 404)

        return jsonify({'message': 'No Answers added.'}), 404
    return jsonify({'message': 'No questions added!'}), 404


@answers.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>',
           methods=['GET'])
def get_answer(questionId, answerId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    if questionsList and answersList:
        answer = [
            {
                'answerId': answer[3],
                'author': answer[4],
                'body': answer[2],
                'prefered': answer[5],
                'QuestionId': answer[1]
            } for answer in answersList if int(answer[3]) == answerId]
            
        return (jsonify(answer[0]), 200) if answer else (Response(json.dumps(['Answer not found!']),
                        status=404, mimetype='application/json'))
    return jsonify({'message': 'Question not found!'}), 404



@answers.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList and questionId in [int(qn[4]) for qn in questionsList]:
            answer_check = valid_answer(request_data)
            if answer_check[0]:
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
                        "error": "Invalid answer data!",
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


@answers.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def select_answer_as_preferred(questionId, answerId):
    current_user = get_jwt_identity()
    if current_user:
        # request_data = request.get_json()
        questionsList = conn.query_all('questions')
        answersList = conn.query_all('answers')

        if answersList and questionsList:

            #answer_check = valid_answer(request_data)
            qtn = [qn[3] for qn in questionsList if int(qn[4]) == questionId]

            answer = [ans for ans in answersList if int(ans[1]) == questionId and int(ans[3]) == answerId]
            
            if qtn and qtn[0] == current_user:

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
                return (response, 201) if answer[0] else (jsonify({'message': 'Answer not found!'}), 404)
            
            return jsonify({'message':
                            f'Only question author:{current_user} can perform this action!'})
        elif not questionsList:
            return jsonify({'message':
                            'Question not found'}), 404

    return jsonify({
        'message': 'To prefer an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401

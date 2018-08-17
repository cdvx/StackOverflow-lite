
from flask import (Flask, redirect, request, flash, session, 
    url_for, jsonify, json, render_template)
from config import Config
import os

from models import (questionsList, Question, answersList, Answer)
from forms import (QuestionForm, AnswerForm)


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)


@app.route('/api/v1/questions', methods=['GET', 'POST'])
def get_questions():
    form = QuestionForm()
    question = Question()
    if (request.method == 'POST'):
        question.id = len(questionsList)
        question.topic = request.form['topic']
        question.body = request.form['body']
        questionsList.append(question.__repr__())

        flash('Question successfully posted')
        return redirect(url_for('get_questions', form=form))
    return render_template('index.html',  form=form, questions=questionsList)



@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET','POST'])
def get_question(questionId):
    form = AnswerForm()
    answer = Answer()
    answers = []
    new_answersList = []
    if request.method == 'POST':
        answer.answerId = len(answersList)
        answer.Qn_Id = int(request.form['Qn_Id'])
        answer.body = request.form['body']
        if valid_answer(answer):
            flash('Answer successfully added.')
            new_answersList.append(answer.__repr__())   
            answersList.append(new_answersList[0])
            return redirect(url_for('get_question', form=form, questionId=questionId))
    for answer in answersList:
        if answer['Qn_Id'] == questionId:
            answers.append(answer)
    return render_template('question.html', answersL=answers, 
        form=form, qId=questionId, questions=questionsList)

def delete_question(question_id):
    pass

@app.route('/api/v1/login')
def login():
    pass
@app.route('/api/v1/signUp')
def signUp():
    pass
@app.route('/api/v1/users/<int:userId>/profile')
def user():
    pass
@app.route('/api/v1/logout')
def logout():
    form = QuestionForm()
    return redirect(url_for('get_questions', form=form))


def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        return True
    else:
        return False
def valid_answer(answerObject):
    if answerObject.Qn_Id and answerObject.body and answerObject.answerId:
        return True
    else:
        return False



if __name__=='__main__':
    app.run(port=5000)


#import flast and other attributes
from flask import (Flask, redirect, request, flash, session, 
    url_for, jsonify, json, render_template)
from config import Config
import os

from questions import questionsList
from forms import QuestionForm
from answers import answersList



app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)



@app.route('/api/v1/questions', methods=['GET', 'POST'])
def get_questions():
    form = QuestionForm()
    question = {}
    if (request.method == 'POST'):
        print('post')

        question['questionId'] = len(questionsList)
        question['topic'] = request.form['topic']
        question['body'] = request.form['body']

        questionsList.append(question)
        # session['questions'] = QL
        flash('Question successfully posted')
        return redirect(url_for('get_questions', form=form))
    print('get')
    return render_template('index.html',  form=form, questions=questionsList)


@app.route('/api/v1/questions/<int:questionId>', methods=['GET', 'POST'])
def get_question(questionId):
    pass


def post_question():
    pass

def post_answer():
    pass

def delete_question(question_id):
    pass

def login():
    pass

def signUp():
    pass

def user():
    pass

def logout():
    pass


def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        return True
    else:
        return False

        


if __name__=='__main__':
    app.run(port=5000)

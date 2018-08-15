#import flast and other attributes
from flask import (Flask, redirect, request, flash, session, 
    url_for, jsonify, json, render_template)
from config import Config
import os

from questions import questionsList, Questions
from forms import QuestionForm



app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)





@app.route('/api/v1/questions', methods=['GET', 'POST'])
def get_questions():
    form = QuestionForm()
    question = {}
    if (request.method == 'POST'):
        if (form.validate_on_submit()):
            with questionsList as QL:
                question['id'] = len(Ql)
                question['topic'] = form.topic.data
                question['body'] = form.body.data
                QL.append(question)
            session['questions'] = QL
            flash('Question successfully posted')
            return redirect(url_for('get_questions', form=form))
    questionsL = []
    for item in questionsList:
        question = {
            'id': item['question_id'],
            'topic': item['topic'],
            'body': item['body']
        }
        # question = Questions(item['question_id'], item['topic'], item['body'])
        questionsL.append(question)
    #questionsL = json.dumps(questionsL)
    return render_template('index.html',  form=form, questions=questionsL)


@app.route('/api/v1/questions/<int:question_id>', methods=['GET', 'POST'])
def get_question(question_id):
    return render_template('question.html')



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

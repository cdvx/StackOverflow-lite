
from flask import Flask, redirect, request, flash
from flask import url_for, jsonify, json, render_template
from questions import questionsList, Questions

app = Flask(__name__)
@app.route('/api/v1/questions')
def get_questions():
    questionsL = []
    for item in questionsList:
        question = Questions(item['question_id'], item['topic'], item['body'])
        questionsL.append(question)
    return render_template('index.html' ,questions=questionsL )


@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    return render_template('question.html')



def post_question():
    pass

def post_answer():
    pass



def validate_question(questionObject):
    if 'question_id' in questionObject and 'topic' in questionObject and 'body' in questionObject:
        return True
    else:
        return False


if __name__=='__main__':
    app.run(port=5000)
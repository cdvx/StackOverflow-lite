from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, 
    SubmitField, TextAreaField, IntegerField, TextField)
from wtforms.validators import (DataRequired, ValidationError, Email, Length, Optional)


class QuestionForm(FlaskForm):
    topic = StringField('Topic', description='Topic')
    body = TextAreaField('Question', description='Enter question here')



class AnswerForm(FlaskForm):
    Qn_Id = IntegerField('Question Id/No.', description='Enter question Id')
    body = StringField('Answer', description='Enter answer here..')
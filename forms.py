from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Optional


class QuestionForm(FlaskForm):
    topic = StringField('Topic', description='Topic')
    body = TextAreaField('Question', description='Enter question here')
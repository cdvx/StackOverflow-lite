from datetime import datetime, timedelta

from flask import (Flask, Response, make_response,
                   json, jsonify, request, url_for, Blueprint)
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash

from app.connect import conn
from app.models import (Answer, Question, User, valid_answer, valid_login_data,
                        valid_question, valid_signup_data, valid_username, valid_email)

from app.utils import ValidationError

# origin = 'https://stackoverflowlite-cdvx-fronted.herokuapp.com'
origin ="*"
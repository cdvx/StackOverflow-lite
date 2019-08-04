from app.routes.imports import *

api = Blueprint("api", __name__)

@api.route('/')
def show_api_works():
    return jsonify({'Welcome to my app': [{'message': "endpoints work"}]})



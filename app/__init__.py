from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config

app = Flask(__name__)

CORS(app)
app.config.from_object('config.Config')
app.config['JWT_SECRET_KEY'] = 'wuiq2739%W%$%^FhjY^^'
jwt = JWTManager(app)

@app.after_request
def after_request(response):
    response.headers.add('Content-Type', 'application/json')
    return response

@app.errorhandler(500)
def internal_server_error(e):
    msg = "Sorry,we are experiencing some technical difficulties"
    msg2 = "Please report this to cedriclusiba@gmail.com and check back with us soon"
    return jsonify({'error': msg, "hint": msg2}), 500


@app.errorhandler(404)
def url_unknown(e):
    msg = "Sorry, resource you are looking for does not exist"
    return jsonify({"error": msg}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    msg = "Sorry, this action is not supported for this url"
    return jsonify({'error': msg}), 405


@app.errorhandler(403)
def forbidden_resource(e):
    msg = "Sorry, resource you are trying to access is forbidden"
    return jsonify({'error': msg}), 403


@app.errorhandler(410)
def deleted_resource(e):
    return jsonify({'error': "Sorry, this resource was deleted"}), 410
import os
from application import create_app
from app.routes import routes
from flask import jsonify


flask_app = create_app(config_=os.getenv('FLASK_ENV'))



if __name__ == '__main__':
    
    flask_app.run(debug=True, port=5000)
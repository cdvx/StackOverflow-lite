from app import app
from app.routes import routes

if __name__ == '__main__':
    app.run(debug=True, port=5000)
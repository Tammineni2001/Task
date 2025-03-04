from flask import Flask, jsonify
from routes.routes import main_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.register_blueprint(main_blueprint)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Data Buddy!"})

if __name__ == '__main__':
    app.run(debug=True)
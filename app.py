from flask import Flask, jsonify
from routes.routes import main_blueprint

app = Flask(__name__)


app.register_blueprint(main_blueprint)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Data Buddy!"})

if __name__ == '__main__':
    app.run(debug=True)
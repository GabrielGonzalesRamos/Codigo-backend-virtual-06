from flask import Flask, request
from dotenv import load_dotenv
from os import environ
app = Flask(__name__)
# dialec
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")


@app.route("/")
def initial_controller():
    return {
        "message": "Welcome  API 🧁" 
    }

if __name__ == '__main__':
    app.run(debug=True)
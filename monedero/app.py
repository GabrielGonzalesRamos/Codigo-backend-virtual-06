from flask import Flask, app, request
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from flask_restful import Api

load_dotenv()


app = Flask(__name__)
print(environ.get("DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_de_datos.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
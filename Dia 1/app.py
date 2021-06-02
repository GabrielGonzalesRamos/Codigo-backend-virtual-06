from flask import Flask, request
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from models.postre import PostreModel
from models.preparacion import PreparacionModel
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
load_dotenv()
app = Flask(__name__)
# dialec
print(environ.get("DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
# Si se establece en True, FLask-SQLAlchemy rastrearan las modificaciones
# de los objetos y lanzará señales.
# Su valor predeterminado es None, igual habilita el tracking pero emite
# una advertencia  que se deshabilitará de manera predeterminada en futuras versiones.
# Esto consume memoria adicional y si no se va a utliizar es mejor desactiviarlo = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# iniciar la bd para darle las credenciales definidas en el config
base_de_datos.init_app(app)

# crea todas las tablas definidas en los modelos en el proyecto
base_de_datos.create_all(app=app)


@app.route("/")
def initial_controller():
    return {
        "message": "Welcome  API 🧁"
    }


if __name__ == '__main__':
    app.run(debug=True)

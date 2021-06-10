from datetime import timedelta
import uuid
from controllers.movimiento import MovimientosController
from flask import Flask, app, request
from dotenv import load_dotenv
from os import environ, path
from config.conexion_bd import base_de_datos
from flask_restful import Api
from controllers.usuario import RegistroController
from controllers.movimiento import MovimientosController
from models.sesion import SesionModel
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from config.custom_jwt import manejo_error_JWT
# Para que en el nombre del archivo que manda el cliente antes de guardarlo, lo valide y evite que se guarde con caracteres
# Especiales que puedan malograr el funcionamiento de la api o guardar de una forma incorrecta
from werkzeug.utils import secure_filename
from uuid import uuid4


load_dotenv()


app = Flask(__name__)
print(environ.get("DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'claveSecreta'
# Para modificar la fecha de caducidad de la token, su valor por defecto es 5 minutos
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=1, seconds=10)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
# para modificar el endpoint del login
app.config['JWT_AUTH_URL_RULE'] = '/login'
# para modificar la llave del username 
app.config['JWT_AUTH_USERNAME_KEY'] = 'correo'
# para modificar la llave del password
app.config['JWT_AUTH_PASSWORD_KEY'] = 'pass'
# 1 byte * 1024 => 1 KB * 1024 => 1 MB * 1024 => 1 GB
# MAX_CONTENT_LENGTH poner un limite  de maximo un 1MB de capacidad
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
jsonwebtoken = JWT(app=app, authentication_handler=autenticador, identity_handler=identificador) # El "autenticador" hace referencia al 
# archivo config.seguridad y la funcion autenticador de la clase Usuario 
# Manejo de error
jsonwebtoken.jwt_error_callback = manejo_error_JWT


base_de_datos.init_app(app)
base_de_datos.create_all(app=app)
EXTENSIONES_PERMITIDAS  = ['png', 'jpg', 'jpeg', 'gif']
#base_de_datos.drop_all(app=app)
api = Api(app)

def archivos_permitidos(filename):
    # recibe dos parametros rsplit el primero es el caracteer a dividir y el segundo 
    # opccional es el que especifica en cuantas partes debe de ser dividido
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in EXTENSIONES_PERMITIDAS



@app.route("/subirArchivo", methods=['POST'])
def subir_archivo():
    print(request.files)
    archivo = request.files['archivo']
    # Para saber el nombre del archivo
    print(archivo.filename)
    # Para saber el tipo de archivo 
    print(archivo.mimetype)
    if archivos_permitidos(archivo.filename):
        # Primero saco el formato del archivo
        formato_archivo = archivo.filename.rsplit(".",1)[-1]

        # Genero un uuid y le agrego la extension
        nombre_archivo = str(uuid4())+'.'+formato_archivo

        # Acá validará que  no existan caracteres especiales que puedan romper el funcionamiento de mi api
        archivo.filename = secure_filename(archivo.filename)
        archivo.save(path.join("multimedia", nombre_archivo))
        return {
            "message": 'Archivo guardado exitosamente' ,
            "success": True
            }, 201
    return {
        "message": 'El archivo no esta permitido only %s' %(EXTENSIONES_PERMITIDAS),
        "success": False
    }, 400

api.add_resource(RegistroController, "/registro")
api.add_resource(MovimientosController, "/movimientos")



if __name__ == '__main__':
    app.run(debug=True)
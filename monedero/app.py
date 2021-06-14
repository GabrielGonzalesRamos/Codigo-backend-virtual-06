from datetime import timedelta
import json
import uuid
from controllers.movimiento import MovimientosController
from flask import Flask, app, request, send_file, render_template # Con el metodo render_template puedo cargar plantillas
from dotenv import load_dotenv
from os import environ, path, remove
from config.conexion_bd import base_de_datos
from flask_restful import Api
from controllers.usuario import RegistroController, ForgotPasswordController, ResetPasswordController
from controllers.movimiento import MovimientosController
from models.sesion import SesionModel
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from config.custom_jwt import manejo_error_JWT
# Para que en el nombre del archivo que manda el cliente antes de guardarlo, lo valide y evite que se guarde con caracteres
# Especiales que puedan malograr el funcionamiento de la api o guardar de una forma incorrecta
from werkzeug.utils import secure_filename
from uuid import uuid4
from flask_cors import CORS
from cryptography.fernet import Fernet
from datetime import datetime

load_dotenv()

UPLOAD_FOLDER = 'multimedia'
app = Flask(__name__)
CORS(app=app)
print(environ.get("DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('JWT_SECRET')
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
        archivo.save(path.join(UPLOAD_FOLDER, nombre_archivo))
        return {
            "message": 'Archivo guardado exitosamente' ,
            "content": request.host_url+'media/'+nombre_archivo,
            "success": True
            }, 201
    return {
        "message": 'El archivo no esta permitido only %s' %(EXTENSIONES_PERMITIDAS),
        "success": False
    }, 400
@app.route("/media/<string:nombre>", methods=['GET'])
def devolver_archivo(nombre):
    try:
        return send_file(path.join(UPLOAD_FOLDER, nombre))
    except:     
        return send_file(path.join(UPLOAD_FOLDER, "not-found.png")), 404

@app.route("/eliminarArchivo/<string:nombre>", methods=['DELETE'])
def eliminar_archivo(nombre):
    try:
        remove(path.join(UPLOAD_FOLDER, nombre))
        return {
            "success": True,
            "content": None,
            "message": 'Archivo eliminado exitosamente'
        }, 201
    except:
        return {
            "success": False,
            "content": None,
            "message": 'El archivo no esta o ya se eliminó'
        }, 404

@app.route("/", methods=['GET'])
def inicio():
    return render_template('base.jinja', mensaje='Retornando desde el PY', texto='Yo soy otro texto')
           
@app.route("/recuperarPassword/<string:token>")
def recuperar_password(token):
    print('Este es el token: ', token)
    fernet = Fernet(environ.get("FERNET_SECRET"))
    # decrypt(b'token')
    # El metodo decrypt recibe una token pero en formato bytes y luego si es que cumple 
    # tendŕá que convertirlo a string usamos el metodo decode
    try:
        respuesta = fernet.decrypt(bytes(token, 'utf-8')).decode('utf-8')
        # La variable respuesta es un string
        # El metodo loads convierte un json a un diccionario
        print('Este token es desencriptado : ', respuesta)
        respuesta_diccionario = json.loads(respuesta)
        fecha_caducidad = datetime.strptime(respuesta_diccionario['fecha_caducidad'], '%Y-%m-%d %H:%M:%S.%f')
        print(respuesta_diccionario)
        if fecha_caducidad > datetime.now():
            print(respuesta_diccionario['correo'])
            return render_template('recovery_password.jinja', correo=respuesta_diccionario['correo']) 
        else:
            return render_template('bad_token.jinja')        
    except Exception as e:
        print(e)
        return render_template('bad_token.jinja')



api.add_resource(RegistroController, "/registro")
api.add_resource(MovimientosController, "/movimientos")
api.add_resource(ForgotPasswordController, "/olvidopassword")
api.add_resource(ResetPasswordController, "/reset-password")
if __name__ == '__main__':
    app.run(debug=True)
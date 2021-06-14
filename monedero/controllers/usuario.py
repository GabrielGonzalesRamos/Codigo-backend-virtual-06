from config.conexion_bd import base_de_datos
from flask_restful import Resource, reqparse, request
from sqlalchemy.sql import expression
from sqlalchemy.exc import IntegrityError
from models.usuario import UsuarioModel
from re import fullmatch, search
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv
import json 
from datetime import date, datetime, timedelta
from utils.enviar_correo_puro import enviarCorreo
import bcrypt

load_dotenv()



PATRON_CORREO = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
PATRON_PASSWORD = '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'


class RegistroController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument( 'nombre', type=str, required=True, help="Ingrese su nombre", location='json')
    serializer.add_argument( 'apellido', type=str, required=True, help="Ingrese su apellido", location='json')
    serializer.add_argument( 'correo', type=str, required=True, help="Ingrese su nombre", location='json')
    serializer.add_argument( 'password', type=str, required=True, help="Ingrese su password", location='json')
    def post(self):
        data = self.serializer.parse_args()
        # Validar si es un correo valido
        correo = data.get('correo')
        # ^ => tiene que coincidir el comienzo de la cadena
        # [a-zA-Z0-9] => significa que el texto tiene que coincidir con una letra miniscula y una letra mayuscula y un numero
        # + => la combinacion del texto anterior se puede repetir más de una vez
        # [@] => que luego si o si tiene que haber un arroba
        # \w => coincida con cualquier caracter alfanumerico
        # [.] => luego si o si tiene que haber un . 
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        password = data.get('password')
        if search(PATRON_CORREO, correo) and fullmatch(PATRON_PASSWORD, password):
            try:
                nuevoUsuario = UsuarioModel(nombre, apellido, correo, password)
                nuevoUsuario.save()
                return {
                    "succes": True,
                    "content": nuevoUsuario.json(),
                    "message": "Usuario registrado exitosamente"
                    }, 201
            except IntegrityError as error:
                print(error)
                return {
                    "succes": True,
                    "content": None,
                    "message": "El correo ya existe"
                }
        else:
            return {
                "succes": True,
                "content": None,
                "message": "Contraseña  o el Correo no cumple con nuestra políticas"
            }, 400

class ForgotPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument("correo", type=str, required=True, location='json', help='Falta el correo')

    def post(self):
        data = self.serializer.parse_args()
        correo = data['correo']
        if search(PATRON_CORREO, correo):
            usuario = base_de_datos.session.query(UsuarioModel).filter_by(usuarioCorreo=correo).first()
            if usuario:
                # inicio mi objeto Fernet con la clave definida en mi variable de entorno
                fernet = Fernet(environ.get("FERNET_SECRET"))
                # El metodo dumps convierte un diccionario a un json 
                payload = {
                    "fecha_caducidad": str(datetime.now() + timedelta(minutes=30)),
                    "correo": correo 
                    }
                print(payload)
                # El metodo dumps convierte en un diccionario a un json
                payload_json = json.dumps(payload)
                # Encripto este payload a un hash listo para mandarlo por el correo
                token = fernet.encrypt(bytes(payload_json, 'utf-8'))
                print(token)
                link = request.host_url+'recuperarPassword/'+token.decode('utf-8')
                if enviarCorreo(usuario.usuarioCorreo, usuario.usuarioNombre, link):
                    return {
                        "succes": True,
                        "content": None,
                        "message": "Revise su bandeja de entrada"
                        }, 201
            else:
                return {
                    "succes": False,
                    "content": None,
                    "message": "El correo no se encuentra registrado en nuestro sistema"
                    }, 403
        else:
            return {
                "succes": False,
                "content": None,
                "message": "El dato enviado no es un correo"
            }, 403

        
class ResetPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument("correo", type=str, required=True, location='json', help='Falta el correo')
    serializer.add_argument( 'password', type=str, required=True, help="Ingrese su password", location='json')
    def post(self):
        data = self.serializer.parse_args()
        if search(PATRON_CORREO, data['correo']):
            usuario = base_de_datos.session.query(UsuarioModel).filter_by(usuarioCorreo=data['correo']).first()
            if usuario:
                if fullmatch(PATRON_PASSWORD, data['password']):
                    print(usuario.usuarioPassword)
                    passwordBytes = bytes(data['password'], "utf-8")
                    passwordHash = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
                    passwordString = passwordHash.decode("utf-8")
                    usuario.usuarioPassword = passwordString
                    print(usuario.usuarioPassword)
                    usuario.save()
                    return {
                        "success": True,
                        "content": usuario.json(),
                        "message": "La contraseña se actulizó exitosamente"
                    }
                else:
                    return {
                        "success": False,
                        "content": None,
                        "message": "La contraseña debe de tener al menos 6 caracteres , una mayus, una minus, un numero y un caracter especial"
                    }
            else:
                return {
                    "succes": False,
                    "content": None,
                    "message": "El dato enviado no es un correo"
                    }, 403

from models.usuario import UsuarioModel
from bcrypt import checkpw
from config.conexion_bd import base_de_datos



class Usuario:
    def __init__(self, id, username):
        self.id = id
        self.username = username
    def __str__(self):
        return "El usuario con el id=%s y username=%s" % (self.id, self.username)     

def autenticador(username, password):
    """ Funcion encargada de validar las credenciales si estas son ingresadas correctamente"""
    if username and password:
        usuario = base_de_datos.session.query(UsuarioModel).filter_by(usurioCorreo=username).first()
        if usuario:
            if checkpw(bytes(password, 'utf-8'), usuario.usuarioPassword):
                return Usuario(usuario.usuarioId, usuario.usuarioCorreo)
            else:
                print("La contraseña no coincide")
                return None    
        else:
            print("El usuario no existe")
            return None        
    else:
        print("Falta el usuario o la password")
        return None

def identificador(payload):
    """ Sirve para que una vez el usuario ya este logeado y tenga su JWT pueda realizar peticiones a una ruta protegida y esta funcion será la encargada de identificar a dicho usuario y devolver su informacion """
    # El payload es un diccionario
    print(payload)
    if(payload['identity']):
        # Se almacena el id del usuario
        usuario = base_de_datos.session.query(UsuarioModel).filter_by(usuarioId = payload['identity']).first()
        if usuario:
            return usuario.json()
        else:
            # El usuario en la token no existe en mi bd 
            return None
    else:
        # En mi payload no hay la llave identity
        return None            


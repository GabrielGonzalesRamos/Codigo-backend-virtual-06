from django.contrib.auth.models import BaseUserManager
# BaseUserManager => modifica el comportamientoi de la creacion de un usuario x consola
class UsuarioManager(BaseUserManager):
    """ Clase que sirve para modificar el comportamiento del modelo auth_user django"""
    def create_user(self, email, nombre, apellido, tipo, password=None):
        """ Creacion de un usuario comun  """
        if not email:
            raise ValueError("El usuario debe tener obligatoriamente un correo")
        # normalizo el correo que aparte de validar si hay un @ y un . ademas lo lleva todo a minusculas (lowercase)     y quita espacios al inicio y al final si es que hubiese
        self.normalize_email(email)
        # creo mi objeto de usuario PERO aún no se guarda en la bd
        nuevoUsuario = self.model(usuarioCorreo = email, usuarioNombre = nombre, usuarioApellido = apellido, usuarioTipo = tipo)
        # Ahora encripto la contraseña
        nuevoUsuario.set_password(password)
        # Guardo en la BD
        nuevoUsuario.save(using=self._db) # Sirve para referenciar a la DB en el caso que nosotros tengamos varias conexiones en nuestro proyecto de django
        return nuevoUsuario
    def create_superuser(self, usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo,  password):
        usuario = self.create_user(usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        
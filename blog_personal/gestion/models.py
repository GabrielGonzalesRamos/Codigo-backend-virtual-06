from django.db import models
from django.db.models import indexes
from django.utils.timezone import now
from datetime import date, datetime

def anio_actual():
    return date.today().year
def opcciones_anio():
    return [(anio, anio) for anio in range(1990, date.today().year + 1)]    



# Create your models here.
class UsuarioModel(models.Model):
    usuarioId = models.AutoField(primary_key=True, null=False, unique=True, db_column='id')
    usuarioNombre = models.CharField(max_length=25, null=False, db_column='nombre',
    # A continuacion son parametros para el panel administrativo
    verbose_name='Nombre del usuario', # Mostrará para que sirve en el form del panel administrativo 
    help_text='Aqui debes ingresar el nombre', # Es el campo de ayuda que se mostrará en el formulario del panel administrativo
    )
    usuarioApellido = models.CharField(max_length=25, null=False, db_column='apellido', verbose_name='Apellido del usuario', help_text='Debes de ingresar el apellido del usuario')
    usuarioCorreo = models.EmailField(max_length=50, db_column='correo', verbose_name='Correo del usuario', help_text='Debes de ingresar un correo valido')
    usuarioDni = models.CharField(max_length=8, db_column='dni', verbose_name='Dni del usuario', help_text='Ingrese un DNI válido')
    def __str__(self):
        return self.usuarioNombre + ' ' + self.usuarioApellido
        
    class Meta:
        # permite pasar metadatos al padre desde el hijo (setear atributos)
        db_table = 'usuarios'
        ordering=['-usuarioCorreo', 'usuarioNombre'] # Modifica el ordenamiento de mis registros de los usuarios
        indexes = [models.Index(fields=['usuarioCorreo', 'usuarioDni'])] # indexacion => indexa cada registro segun una columnao columnas en especifico
        unique_together =  [['usuarioCorreo', 'usuarioDni', 'usuarioNombre']] # Sirve para hacer unica una conjugacion de una o más columnas 
        verbose_name = "usuario" # sirve para el panel administrativo es el nombre que se mostrara en vez del nombre de la clase
        verbose_name_plural="usuarios" # el nombre pero en plural para los registros


class LibroModel(models.Model):
    libroId = models.AutoField(primary_key=True, null=False, unique=True, db_column='id')
    libroNombre = models.CharField(max_length=45, null=False, db_column='nombre', verbose_name='Nombre del libro', help_text='Ingrese un nombre valido')
    libroEdicion = models.IntegerField(db_column='edicion', null=False, choices=opcciones_anio(), verbose_name='Año de edicion', help_text='Ingrese el año de la edicion', default=anio_actual, )
    libroAutor = models.TextField(db_column='autor', null=False, verbose_name='Autor del libro', help_text='Ingrese el autor')
    libroCantidad = models.IntegerField(db_column='cantidad', verbose_name='Cantidad', default=0)
    # La fecha y hora actual cuando se cree el registro
    createAt = models.DateTimeField(auto_now_add=True, db_column='created_at', null=False)
    # auto_now = > toma la hora actual cada vez que se modifique un registro
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at', null=False)
    deleteAt = models.DateTimeField(db_column='deleted_at', null=True)
    def __str__(self):
        return self.libroNombre

    class Meta:
        db_table = 'libros'
        unique_together = [['libroNombre', 'libroEdicion', 'libroAutor']]
        verbose_name = 'libro'
        verbose_name_plural = 'libros'
        ordering=['-libroEdicion', '-libroCantidad', 'libroNombre']

class PrestamoModel(models.Model):
    prestamoId = models.AutoField(primary_key=True, unique=True, db_column='id')
    prestamoFechaInicio = models.DateField(default=date.today, db_column='fecha_inicio', verbose_name='Fecha de inicio del prestamo')
    prestamoFechaFin = models.DateField(db_column='fecha_fin', verbose_name='Fecha de fin del prestamo', null=False)
    prestamoEstado = models.BooleanField(default=True, db_column='estado', verbose_name='Estado del prestamo', help_text='Indique el estado del prestamo')
    # opcciones para la eliminacion de una PK con relacion 
    # CASCADE => se elimina primero la pk y luego las fk' s
    # PROTECT => no permite la eliminacion de la pk si tiene relaciones
    # SET_NULL => elimina la pk y posteriormente  todas sus fk cambian de valor a null
    # DO_NOTHING => elimina la pk y aún mantiene el valor de sus fk (mala integridad)
    # RESTRICT => no permite la eliminacion como el protect pero lanzará un error de tipo RestrictedError

    # related_name : servirá para poder acceder desde la clase 
    usuario = models.ForeignKey(to=UsuarioModel, db_column='usuario_id', on_delete=models.CASCADE, related_name='usuarioPrestamos', verbose_name='Usuario', help_text='Seleccione el usuario a prestar' ) 
    libro  = models.ForeignKey(to=LibroModel, db_column='libro_id', on_delete=models.PROTECT, related_name='libroPrestamos', verbose_name='Libro', help_text='Seleccione el libro a prestar')      
    
    class Meta:
        db_table = 'prestamos'
        verbose_name = 'prestamo'
        verbose_name_plural = 'prestamos'
        ordering = ['-prestamoFechaFin']
        
        
        

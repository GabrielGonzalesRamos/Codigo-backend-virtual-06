from typing import Tuple
from django import db
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .authManager import UsuarioManager
from django.utils.timezone import now


class PlatoModel(models.Model):
    patoId = models.AutoField(primary_key=True, null=False, db_column='id', unique=True)
    platoNombre = models.CharField(max_length=45, null=False, db_column='nombre', unique=True)
    platoPrecio = models.DecimalField(db_column='precio', null=False, max_digits=5, decimal_places=2)
    # ImageField => sirve para almacenar imagenes EN EL SERVIDOR, en la db guardará la ubicacion del archivo y el archivo lo almacenará en el propio servidor
    platoFoto = models.ImageField(upload_to='platos/', db_column='foto', null=True)
    platoCantidad = models.IntegerField(db_column='cantidad', default=0)
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at', null=False)
    # El campo es opccional, PERO si el cliente no ingresa la data, el valor por defecto será 0
    class Meta:
        db_table = 'platos'
        ordering = ['platoNombre']

class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    """ Modificar el modelo auth_user de la Base de Datos"""
    # Si se desea modificar solamente los campos necesarios del modelo auth_user, se tendrá que usar el AbstractUser (first_name, last_name, password)
    # Si se desea resetear por completo mi auth_use usar el AbstractBaseUser
    # PermissionsMixin => es la clase encargada de dar todos los permisos a nivel panel administrativo
    TIPO_PERSONAL = [
        (1, 'ADMINISTRADOR'),
        (2, 'CAJERO'),
        (3, 'MOZO')
    ]
    usuarioId = models.AutoField(primary_key=True, unique=True, db_column='id')
    usuarioNombre = models.CharField(max_length=20, null=False, db_column='nombre', verbose_name='Nombre del usuario')
    usuarioApellido = models.CharField(max_length=20, null=False, db_column='apellido', verbose_name='Apellido del usuario')
    usuarioCorreo = models.EmailField(db_column='correo', null=False, unique=True, verbose_name='Correo del usuario')
    password = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    usuarioTipo = models.IntegerField(choices=TIPO_PERSONAL, db_column='tipo', verbose_name='Tipo del usuario')
    usuarioTelefono = models.CharField(max_length=10, db_column='telefono')
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at', null=False)
    # Comportamiento del modelo al momento de realizar la creacion del superuser x consola
    objects = UsuarioManager()
    # Ahora defino que columna será la encargada de validar que el usuario sea único
    USERNAME_FIELD = 'usuarioCorreo'
    # Indica que campos se van a solicitar cuando se cree al superuser por consola
    REQUIRED_FIELDS = ['usuarioNombre', 'usuarioApellido', 'usuarioTipo']
    class Meta:
        db_table = 'usuarios'

class MesaModel(models.Model):
    mesaId = models.AutoField(primary_key=True, unique=True, null=False, db_column='id')
    mesaDescripcion = models.CharField(max_length=10, null=False, db_column='descripcion')
    mesaCapacidad = models.IntegerField(db_column='capacidad', null=False)
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at', null=False)
    class Meta:
        db_table = 'mesas'

class PedidoModel(models.Model):
    pedidoId = models.AutoField(primary_key=True, unique=True, db_column='id')
    pedidoFecha = models.DateTimeField(auto_now=True, db_column='fecha')
    pedidoTotal = models.DecimalField(db_column='total', max_digits=5, decimal_places=2)
    pedidoNombreCliente = models.CharField(max_length=45, db_column='nombre_cliente')
    pedidoDocumentoCliente = models.CharField(max_length=12, db_column='documento_cliente')

    usuario = models.ForeignKey(to=UsuarioModel, db_column='usuario_id', on_delete=models.PROTECT, related_name = 'usuarioPedidos' )
    mesa = models.ForeignKey(to=MesaModel, on_delete=models.PROTECT, related_name='mesaPedidos', db_column='mesa_id')
    class Meta:
        db_table = 'pedidos'
        ordering = ['-pedidoFecha']

class DetalleModel(models.Model):
    detalleId = models.AutoField(primary_key=True, db_column='id', unique=True, null=False)
    detalleCantidad = models.IntegerField(db_column='cantidad', null=False)
    detalleSubtotal = models.DecimalField(max_digits=5, decimal_places=2, db_column='sub_total')

    pedido = models.ForeignKey(to=PedidoModel, db_column='pedido_id', on_delete=models.PROTECT, related_name='pedidoDetalles')
    plato = models.ForeignKey(to=PlatoModel, db_column='plato_id', on_delete=models.PROTECT, related_name='platoDetalles')

    class Meta:
        db_table = 'detalles'
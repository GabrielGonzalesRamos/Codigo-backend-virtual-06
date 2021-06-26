
from django.db.models import fields
from rest_framework.generics import CreateAPIView
from rest_framework.validators import ProhibitSurrogateCharactersValidator
from .models import *
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from os import path, write
import os
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PlatoSerializer(serializers.ModelSerializer):
    platoFoto = serializers.CharField(max_length=100)
    class Meta:
        model = PlatoModel
        fields = '__all__'


class ArchivoSerializer(serializers.Serializer):
    # max_length > Indica el tamaño maximo del NOMBRE del archivo
    # use_url > Si es True, entonces el valor de la URL será usado para mostar la ubicacion del arhivo, si es False entonces se usará el nombre del arhicov para su 
    # Representacion , su valor por defecto es UPLOADED_FILES_USE_URL que significa True en la configuración interna de DRF
    archivo = serializers.ImageField(max_length=5*1024*1024, use_url=True)
    def save(self):
        print(self.validated_data)
        archivo : InMemoryUploadedFile = self.validated_data.get('archivo')
        # Para ver el tipo de archivo que es 
        #print(archivo.content_type)
        # Para ver el nombre del archivo 
        print(archivo.name)
        # Para ver el tamaño del archivo (En Bytes)
        #print(archivo.size)
        # Para leer el archivo
        # Una vez que se lee el archivo se elimina su informacion
        # print(archivo.read)
        ruta = default_storage.save(archivo.name, ContentFile(archivo.read()))
        ruta_final = path.join(settings.MEDIA_ROOT, ruta)
        return settings.MEDIA_URL + ruta
        #print(ruta_final)

class EliminarImagenSerializer(serializers.Serializer):
    nombre = serializers.CharField()

class CustomPayloadSerializer(TokenObtainPairSerializer):
    # Funcion incorporada en python que devuelve un método de la clase de la cual se esta heredando
    # El metodo recibirá la clase como primer argumento, cuando se llama a este método, se pasa a la clase como primer argumento
    @classmethod
    def get_token(cls, user: UsuarioModel):
        token = super(CustomPayloadSerializer, cls).get_token(user)
        print(token)
        token['usuarioTipo'] = user.usuarioTipo
        token['user_mail'] = user.usuarioCorreo
        token['mensaje'] = 'Saludos'
        return token

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    # Forma 1 para modificar algun atributo del model
    # password = serializers.CharField(write_only=True)
    def save(self):
        usuarioNombre = self.validated_data.get('usuarioNombre')
        usuarioApellido = self.validated_data.get('usuarioApellido')
        usuarioCorreo = self.validated_data.get('usuarioCorreo')
        usuarioTipo = self.validated_data.get('usuarioTipo')
        usuarioTelefono = self.validated_data.get('usuarioTelefono')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(usuarioNombre = usuarioNombre, usuarioApellido = usuarioApellido, usuarioCorreo = usuarioCorreo, usuarioTipo = usuarioTipo, usuarioTelefono = usuarioTelefono ) 
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()
        return nuevoUsuario
    class Meta:
        model =  UsuarioModel
        exclude = ['groups', 'user_permissions']
        # extra_kwargs => Es para dar configuracion adicional a los atributos de un model serializer
        # usanado el atributo extra_kwargs se puede editar las configuraciones de si solo escitura, solo lectura, 
        # required, allow null, default y error messages
        # No es necesario volver a declarar las mimas configuraciones inciales
        extra_kwargs = {
            'password' : {
                'write_only': True
            }
        }

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesaModel
        fields = '__all__'

class DetalleSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    plato = serializers.IntegerField(min_value=1)

class PedidoSerializer(serializers.Serializer):
    detalle = DetalleSerializer(many = True)
    documento_cliente = serializers.CharField(required=False, min_length=8, max_length=11)
    mesa = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if data.get('documento_cliente') and (len(data.get('documento_cliente')) == 8 or len(data.get('documento_cliente')) == 11):
            return data
        if data.get('documento_cliente') is None:
            return data
        raise serializers.ValidationError( detail='El documento debe de ser de 8 o 11 caracteres')        
    


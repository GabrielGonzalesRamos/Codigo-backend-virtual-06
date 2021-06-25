from django.db.models import fields
from .models import *
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from os import path

class PlatoSerializer(serializers.ModelSerializer):
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
        print(archivo.content_type)
        # Para ver el nombre del archivo 
        print(archivo.name)
        # Para ver el tamaño del archivo (En Bytes)
        print(archivo.size)
        # Para leer el archivo
        # print(archivo.read)
        ruta = default_storage.save(archivo.name, ContentFile(archivo.read()))
        ruta_final = path.join(settings.MEDIA_ROOT, ruta)
        print(ruta)
        print(ruta_final)
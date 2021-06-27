from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import PlatoModel
from rest_framework.request import Request
from rest_framework.generics import DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from .serializers import *
from rest_framework import status
from django.conf import settings
import os
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
import requests
from os import environ
from dotenv import load_dotenv
load_dotenv()


class PaginacionPersonalizada(PageNumberPagination):
    page_query_param='pagina' # Es el nombre de la variable que usaremos en la paginacion, su valor por default es page
    page_size = 2 # Es el valor predeterminado para la cantidad de items por pagina
    page_size_query_param='cantidad' # Es el nombre de la variable que usamores para la cantidad de elementos que el usuarios desea
    max_page_size = 5 # Si el usuario me manda un elemento mayor que el max_page_size entonces usaremos el max_page_size (El tope de elementos por hoja)
    def get_paginated_response(self, data):
        return Response(data={
            'paginacion': {
                'paginaContinua': self.get_next_link(),
                'paginaPrevia': self.get_previous_link(),
                'total': self.page.paginator.count,
            },
            'data': {
                'success': True,
                'content': data,
                'message': None
            }
        }, status=status.HTTP_200_OK)



class ArchivosController(CreateAPIView):
    serializer_class = ArchivoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.FILES)
        if data.is_valid():
            url = request.META.get('HTTP_HOST')
            archivo = data.save()
            print(archivo)
            #print(data.validated_data)
            return Response({
                "success": True,
                "content": url + archivo,
                "message": "Archivo subido exitosamente"
                }, status=status.HTTP_201_CREATED)
        else: 
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Error al subir el archivo"
            }, status=status.HTTP_400_BAD_REQUEST)

class EliminarArchivoController(DestroyAPIView):
    serializer_class = EliminarImagenSerializer

    def delete(self, request):
        data = self.serializer_class(data=request.data)
        try:
            if data.is_valid():
                os.remove(settings.MEDIA_ROOT / data.validated_data.get('nombre'))
                return Response(data={
                    "success": True,
                    "content": None,
                    "message": "Imagen eliminada"
                    })
            else:
                return Response(data={
                    "success": False,
                    "content": data.errors,
                    "message": "Error al eliminar la imagen"
                    })
        except:
            return Response(data={
                "success": False,
                "content": None,
                "message": "Imagen ya fue eliminada previamente o no existe"
            })

class PlatosController(ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                "success": True,
                "content": data.data,
                "message": "Plato Creado Exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Error al crear el plato"
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomPayloadController(TokenObtainPairView):
    """ Sirve  para modifcar el payload de la token de acceso"""   
    permission_classes = [AllowAny]
    serializer_class = CustomPayloadSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        print(data.initial_data)
        if data.is_valid():
            print(data.validated_data)
            return Response(data={
                "success": True,
                "content": data.validated_data,
                "message": "Login exitoso"
            })
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Error de generacion de la JWT"
            })    

class RegistroUsuarioController(CreateAPIView):
    serializer_class = RegistroUsuarioSerializer
    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response({
                "message": "Usuario Creado Exitosamente",
                "content": data.data,
                "success": True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Error al crear usuario",
                "content": data.errors,
                "success": False
            })

class MesaController(ListAPIView):
    queryset = MesaModel.objects.all()
    pagination_class = PaginacionPersonalizada
    serializer_class = MesaSerializer


class PedidoController(CreateAPIView):
    serializer_class = PedidoSerializer
    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            print(data.validated_data)
            if data.validated_data.get('documento_cliente'):
                print(data.validated_data.get('documento_cliente'))
                if len(data.validated_data.get('documento_cliente')) == 8:
                    url = "https://apiperu.dev/api/dni/{}".format(data.validated_data.get('documento_cliente'))
                    print('es un dni')
                elif len(data.validated_data.get('documento_cliente')) == 11:
                    url = "https://apiperu.dev/api/ruc/{}".format(data.validated_data.get('documento_cliente'))
                    print('es un dni')
                headers = {
                    "Authorization": environ.get('TOKEN'),
                    "Content-Type": "application/json"
                    }
                respuesta = requests.get(url=url, headers=headers)
                print(respuesta.ok)
                print(respuesta.json())
                print(respuesta.status_code)                 
            return Response(data={
                "success": True,
                "content": data.data,
                "message": "Pedido creado correctamente"
            })
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Error al crear el pedido"
            })    
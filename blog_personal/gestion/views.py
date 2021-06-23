from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.timezone import now
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from .models import LibroModel, PrestamoModel, UsuarioModel
from .serializers import LibroSerializer, BusquedaLibroSerializer, UsuarioSerializer, PrestamoSerializer, PrestamoNestedSerializer, PrestamoUsuarioSerializer, UserPrestamoSerializer

from rest_framework.pagination import PageNumberPagination

class PaginacionPersonalizada(PageNumberPagination):
    page_query_param='pagina' # Es el nombre de la variable que usaremos en la paginacion, su valor por default es page
    page_size = 50 # Es el valor predeterminado para la cantidad de items por pagina
    page_size_query_param='cantidad' # Es el nombre de la variable que usamores para la cantidad de elementos que el usuarios desea
    max_page_size = 50 # Si el usuario me manda un elemento mayor que el max_page_size entonces usaremos el max_page_size (El tope de elementos por hoja)
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

# Crear y Listar todos los libros
class LibrosController(ListCreateAPIView):
#class LibrosController(ListAPIView):
    # Todas las clases genericas necesitan un query_set y un serializer_class
    # El queryset = Es la consulta que se hará a la BD cuando se llame a esta clase de un determinado método
    queryset = LibroModel.objects.all() # SELECT * FROM libros;
    # El serializer class es el encargado de transformar la data que llega y que se envia al cliente
    serializer_class = LibroSerializer
    pagination_class = PaginacionPersonalizada
    # def get(self, request):
    #     # En el request se almacena todos los datos que manda el front(headers, body, cookies, auth)
    #     print(self.get_queryset())
    #     respuesta = self.serializer_class(instance=self.get_queryset(), many=True)
    #     print(respuesta.data)
    #     return Response(data={
    #         'success': True,
    #         'content': respuesta.data,
    #         'message': None
    #     }, status=200, )



    def post(self, request: Request):
        # La informacion adjuntada en el body se recibirá por el atributo "data"
        print(request.data)
        print(self.serializer_class(data=request.data))
        data = self.serializer_class(data=request.data)
        # El metodo is_valid() validará si la data enviada es o no correcta, es decir, si cumple con los requisitos para crear un nuevo libro, esto retorna un BOOL (True | False)
        # Adicionalmente podemos indicar un parametro llamado raise_exception => True
        # Automaticamente lanzará los errores que no permiten que la data sea valida
        # Por defecto el valor es False
        print(self.serializer_class(data=request.data).is_valid())

        valida = data.is_valid()
        if valida:
            # El metodo save() corresponde al serializador que cuando es de tipo ModelSerializer implemente los metodos de guardado y actulizacion en la BD
            data.save()
            # El atributo data, nos dará un diccionario ordenado con la informacion guardada en la BD (incluyendo campos de solo lectura => id) 
            return Response(data= {
                'success': True,
                'content': data.data,
                'message': 'Libro creado exitosamente'
                }, status=status.HTTP_201_CREATED)
        else:
            # El atributo errors me indicará todos los errores que no han permitido que la informacion sea valida
            return Response(data={
                'success': False,
                'content': data.errors,
                'message': 'La data no es valida'
            }, status=status.HTTP_400_BAD_REQUEST
            )        

class LibroController(RetrieveUpdateDestroyAPIView):
    queryset = LibroModel.objects.all()
    serializer_class = LibroSerializer

    def get(self, request: Request, id):
        libro = LibroModel.objects.filter(libroId = id).first()
        pruebaLibro = LibroModel.objects.values('libroId', 'libroNombre', 'libroEdicion', 'libroAutor', 'libroCantidad').filter(libroId = id).first
        print(pruebaLibro)
        print(libro)
        if libro is not None:
            libroSerializable = self.serializer_class(instance=libro)
            return Response(data={
                "success": True,
                "content": libroSerializable.data,
                "message": None
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "success": False,
                "content": None,
                "message": 'Libro no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)    

    def put(self, request: Request, id):
        libro = LibroModel.objects.filter(libroId = id).first()
        if libro:
            data = self.serializer_class(data=request.data)
            # initial_data => retorna todos los campos que hace match con el modelo PERO no valida
            # Las funciones de unique_together ni los indices ni los campos unique
            # Si queremos 'pasarnos de vivos' y actualizar un registro con otro saltandonos las reglas del unique_together
            # Igual no se podrá porque ahí la BD entrará a trabajar directamente a pesar que en el ORM lo permitase
            libro_actualizado = self.serializer_class().update(instance=libro, validated_data=data.initial_data)
            print(libro_actualizado)
            return Response(data='ok')
        else:
            return Response(data={
                "message": "No se encontro el libro",
                "content": None,
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)                

    def delete(self, request: Request, id):
        libro = LibroModel.objects.filter(pk=id).first()
        libro.deleteAt = now()
        libro.save()
        data = self.serializer_class(instance=libro)
        return Response(data={
            "success": True,
            "content": data.data,
            "message": "Se inhabilitó el libro exitosamente"
        })
        

@api_view(http_method_names=['GET'])
def busqueda_libros(request: Request):
    print(request.query_params)
    nombre = request.query_params.get('nombre')
    autor = request.query_params.get('autor')
    resultado = LibroModel.objects.filter(
    libroNombre__contains = nombre if nombre else '', 
    libroAutor__contains = autor if autor else ''
    ).order_by('libroNombre').all()
    # if nombre and autor:
    #     resultado = LibroModel.objects.filter(libroNombre__contains = nombre, libroAutor___contains = autor).order_by
    # # SELECT * FROM LIBROS WHERE LIBRONOMBRE LIKE '% +nombre+ %'
    # resultado = LibroModel.objects.filter(libroNombre__contains=nombre).order_by('libroNombre').all()
    resultado_serializado = LibroSerializer(instance=resultado, many=True)
    # print(resultado)
    return Response(data={
        "success": True,
        "content": resultado_serializado.data,
        "message": None
    })

@api_view(http_method_names=['GET', 'POST'])
def buscador_edicion(request: Request):
    if request.method == 'POST':
        print('aca va el post')
        return Response(data={
            "success": False,
            "content": None,
            "message": "Metodo incorrecto!"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == 'GET':
        parametros_serializado = BusquedaLibroSerializer(data=request.query_params)
        if parametros_serializado.is_valid():
            print(parametros_serializado.validated_data)
            libros = LibroModel.objects.filter(libroEdicion__range=(parametros_serializado.validated_data.get('inicio'), parametros_serializado.validated_data.get('fin')))
            libroSerializado = LibroSerializer(instance=libros, many=True)
            return Response(data={
                "success": True,
                "message": None,
                "content": libroSerializado.data
            })
        else:
            return Response(data={
                "success": False,
                "message": parametros_serializado.errors,
                "content": None
            }, status=status.HTTP_402_PAYMENT_REQUIRED)    


class UsuariosController(ListCreateAPIView):
    queryset = UsuarioModel.objects.all()
    serializer_class = UsuarioSerializer
    pagination_class = PaginacionPersonalizada


class PrestamosController(CreateAPIView):
    queryset = PrestamoModel.objects.all()
    serializer_class =  PrestamoSerializer
    def post(self, request: Request):
        data = request.data
        nuevoPrestamo = PrestamoSerializer(data=data)
        if nuevoPrestamo.is_valid():
            respuesta = nuevoPrestamo.save()
            print(type(respuesta))
            if type(respuesta) is PrestamoModel:
                return Response(data={
                    "sucess": True,
                    "content": nuevoPrestamo.data,
                    "message": "Prestamo agregado exitosamente"
                    }, status=status.HTTP_201_CREATED)
        return Response(data={
            "success": False,
            "content": nuevoPrestamo.errors or (respuesta if type(respuesta) is str else respuesta.args),
            "message": "Error al crear el prestamo"
            }, status=status.HTTP_400_BAD_REQUEST)


class PrestamoController(RetrieveAPIView):
    queryset = PrestamoModel.objects.all()
    serializer_class =  PrestamoUsuarioSerializer

    def get(self, request, id):
        # Primero validar si el prestamos existe o no existe
        prestamo = PrestamoModel.objects.filter(prestamoId = id).first() 
        if prestamo:
            data = self.serializer_class(instance=prestamo)
            return Response(data={
                "success": True,
                "content": data.data,
                "message": None

            })
        else:
            return Response(data={
                "success": False,
                "content": None,
                "message": "Prestamo no existe"
            }, status=status.HTTP_404_NOT_FOUND)
        pass

class  UsuarioController(RetrieveAPIView):
    #queryset = UsuarioModel.objects.all()
    serializer_class = UserPrestamoSerializer

    def get(self, request, id):
        usuario = UsuarioModel.objects.filter(usuarioId = id).first()
        if usuario:
            data = self.serializer_class(instance=usuario)
            return Response(data={
                "success": True,
                "content": data.data,
                "message": None
            }, status=status.HTTP_200_OK)
        else:
                        return Response(data={
                "success": False,
                "content": None,
                "message": "Usuario no existe"
            }, status=status.HTTP_404_NOT_FOUND) 
        
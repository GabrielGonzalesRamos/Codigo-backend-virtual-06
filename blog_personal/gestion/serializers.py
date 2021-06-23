from copy import error
from datetime import date

from django.db import models
from .models import LibroModel, PrestamoModel, UsuarioModel
from rest_framework import fields, request, serializers
from django.utils.timezone import now
from django.db import transaction, Error

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        # model => Definir a que modelo se basará para la serialización
        model = LibroModel
        # fields => Indica los campos que serán necesarios para el funcionamiento de este serializer
        # Si se desea usar una minoria del columnas se declarará en una lista o tupla
        # fields = ['col1'] |  fields = ('col1')
        #fields = '__all__'
        exclude = ['deleteAt']
        # exclude => Excluirá la o las columnas definidas
        # exclude = ['libroId']
        # NOTA no se puede usar a la vez el atributo fields con el atributo exclude
        # NOTA en el exclude no  existe la opccion '__all__'

class BusquedaLibroSerializer(serializers.Serializer):
    inicio = serializers.IntegerField(required=True, help_text="Ingrese la fecha de inicio", min_value=1990, max_value=now().year, error_messages = {
        'incorrect_type': 'Tipo de dato incorrecto, se esperaba un int pero se mando un {input_type}',
        'required': 'Falta el inico',
        'invalid': 'Tipo de dato incorrecto, se esperaba un int pero se mando un string',
        'max_value': 'Error el valor maximo es {max_value}',
        'min_value': 'Error el valor minimo es {min_value}'
    })
    fin = serializers.IntegerField(required=True, help_text="Ingrese la fecha fin", min_value=1990, max_value=now().year )

    def validate(self, data):
        print(data)
        """ Metodo que se ejecutará cuando nosotros llamemos al metodo is_valid() """
        if data.get('inicio') <= data.get('fin'):
            return data
        raise serializers.ValidationError(detail='La fecha inicio debe de ser menor que fin')    

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        fields = '__all__'        

class  PrestamoSerializer(serializers.ModelSerializer):
    def validate(self, data):
        prestamoActivo = PrestamoModel.objects.filter(usuario=self.initial_data.get('usuario'), prestamoEstado=True).first()
        print(prestamoActivo)
        if prestamoActivo:
            raise serializers.ValidationError({'usuario': "El usuario tiene un prestamo activo"})
        libro = LibroModel.objects.filter(libroId=self.initial_data.get('libro')).first()
        if libro.deleteAt:
            raise serializers.ValidationError({'prestamo': "El libro no esta disponible"})
        return data
    def save(self):
        # libro: LibroModel = LibroModel.objects.filter(libroId = self.validated_data.get('libro')).first()
        # usuario: UsuarioModel = UsuarioModel.objects.filter(usuario = self.validated_data.get('usuario')).first()
        if self.validated_data.get('libro').libroCantidad > 0:
            try:
                with transaction.atomic(): # Creamos una transaccion 
                    # prestamoActivo = PrestamoModel.objects.filter(usuario = self.validated_data.get('usuario').usuarioId, prestamoEstado = True).first()
                    # if prestamoActivo:
                    #     return "El usuario tiene un prestamo activo"
                    # libro =  LibroModel.objects.filter(libroId = self.validated_data.get('libro').libroId).first()
                    # if libro.deleteAt:
                    #     return "El libro no esta disponible" 
                    self.validated_data.get('libro').libroCantidad = self.validated_data.get('libro').libroCantidad - 1
                    self.validated_data.get('libro').save()
                    nuevoPrestamo = PrestamoModel(
                        prestamoFechaInicio = self.validated_data.get('prestamoFechaInicio', date.today()),
                        prestamoFechaFin = self.validated_data.get('prestamoFechaFin'),
                        prestamoEstado = self.validated_data.get('prestamoEstado', True),
                        usuario = self.validated_data.get('usuario'),
                        libro = self.validated_data.get('libro')
                        )
                    nuevoPrestamo.save()
                    return nuevoPrestamo
            except Error as error:
                print(error)
                return None
            # Retornamos el nuevo prestamo creado    
        else:
            # Lanzaremos un error de validacion cuando no exista el libro 0 el usuario
            return 'El libro no tiene suficientes unidaddes'
    class Meta:
        model = PrestamoModel
        fields = '__all__'

class PrestamoNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoModel
        fields = '__all__'
        # Con el atributo depth se indica cuantos niveles quiere ingresar a partir del actual
        depth = 1

class PrestamoUsuarioSerializer(serializers.ModelSerializer):
    usurio_pertenece = UsuarioSerializer(source="usuario")
    class Meta:
        model = PrestamoModel
        fields = '__all__'


class UserPrestamoSerializer(serializers.ModelSerializer):
    #usuarioPrestamos = PrestamoNestedSerializer(many=True)
    prestamos = PrestamoNestedSerializer(source = "usuarioPrestamos", many=True)
    class Meta:
        model = UsuarioModel
        fields = '__all__'